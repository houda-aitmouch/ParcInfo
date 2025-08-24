from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
import requests
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from typing import List, Dict
from django.http import JsonResponse
from django.db.models import Q

from apps.commande_bureau.models import CommandeBureau
from apps.commande_informatique.models import Commande
# Imports avec gestion d'erreurs pour la recherche globale
try:
    from apps.materiel_informatique.models import MaterielInformatique
except ImportError:
    MaterielInformatique = None

try:
    from apps.materiel_bureautique.models import MaterielBureau
except ImportError:
    MaterielBureau = None

try:
    from apps.commande_informatique.models import Commande
except ImportError:
    Commande = None

try:
    from apps.commande_bureau.models import CommandeBureau
except ImportError:
    CommandeBureau = None

try:
    from apps.fournisseurs.models import Fournisseur
except ImportError:
    Fournisseur = None

try:
    from apps.demande_equipement.models import DemandeEquipement
except ImportError:
    DemandeEquipement = None

from apps.livraison.models import Livraison

logger = logging.getLogger(__name__)

def get_warranty_notifications():
    """
    Récupère les garanties qui expirent dans moins d'un mois
    """
    today = datetime.now().date()
    one_month_later = today + timedelta(days=30)
    
    notifications = []
    
    # Vérifier les garanties des matériels informatiques
    materiels_it = MaterielInformatique.objects.select_related(
        'ligne_commande__commande__fournisseur',
        'ligne_commande__designation',
        'ligne_commande__description'
    ).all()
    
    for materiel in materiels_it:
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie:
            jours_restants = (date_fin_garantie - today).days
            if 0 <= jours_restants <= 30:
                notifications.append({
                    'type': 'garantie_expiration',
                    'titre': f'Garantie expire dans {jours_restants} jours',
                    'description': f'Matériel IT: {materiel.ligne_commande.designation.nom} - {materiel.ligne_commande.description.nom}',
                    'details': (
                        f"Code: {materiel.code_inventaire}, "
                        f"Fournisseur: {materiel.ligne_commande.commande.fournisseur.nom}, "
                        f"Commande: {materiel.ligne_commande.commande.numero_commande}"
                    ),
                    'urgence': 'urgente' if jours_restants <= 7 else 'attention',
                    'jours_restants': jours_restants,
                    'date_expiration': date_fin_garantie,
                    'timestamp': f'Il y a {max(0, (today - date_fin_garantie).days)} jours'
                })
    
    # Vérifier les garanties des matériels bureautiques
    materiels_bureau = MaterielBureau.objects.select_related(
        'ligne_commande__commande__fournisseur',
        'ligne_commande__designation',
        'ligne_commande__description'
    ).all()
    
    for materiel in materiels_bureau:
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie:
            jours_restants = (date_fin_garantie - today).days
            if 0 <= jours_restants <= 30:
                notifications.append({
                    'type': 'garantie_expiration',
                    'titre': f'Garantie expire dans {jours_restants} jours',
                    'description': f'Matériel Bureau: {materiel.ligne_commande.designation.nom} - {materiel.ligne_commande.description.nom}',
                    'details': (
                        f"Code: {materiel.code_inventaire}, "
                        f"Fournisseur: {materiel.ligne_commande.commande.fournisseur.nom}, "
                        f"Commande: {materiel.ligne_commande.commande.numero_commande}"
                    ),
                    'urgence': 'urgente' if jours_restants <= 7 else 'attention',
                    'jours_restants': jours_restants,
                    'date_expiration': date_fin_garantie,
                    'timestamp': f'Il y a {max(0, (today - date_fin_garantie).days)} jours'
                })
    
    # Trier par urgence (urgente d'abord, puis par jours restants)
    notifications.sort(key=lambda x: (x['urgence'] != 'urgente', x['jours_restants']))
    
    return notifications

def warranty_notifications_json(request):
    """
    Vue pour récupérer les notifications de garantie en JSON selon le rôle de l'utilisateur
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Superadmin reçoit toutes les notifications (Bureau + Informatique)
            notifications_bureau = build_upcoming_warranty_notifications_for_bureau()
            notifications_info = build_upcoming_warranty_notifications_for_info()
            notifications = notifications_bureau + notifications_info
        elif request.user.groups.filter(name='Gestionnaire Informatique').exists():
            # Gestionnaire info reçoit seulement les notifications informatiques
            notifications = build_upcoming_warranty_notifications_for_info()
        elif request.user.groups.filter(name='Gestionnaire Bureau').exists():
            # Gestionnaire bureau reçoit seulement les notifications bureautiques
            notifications = build_upcoming_warranty_notifications_for_bureau()
        else:
            # Employés ne reçoivent pas de notifications de garantie
            notifications = []
        
        return JsonResponse({
            'notifications': notifications,
            'count': len(notifications)
        })
    return JsonResponse({'notifications': [], 'count': 0})

def calculate_garantie_end_date(date_reception, duree_valeur, duree_unite):
    """Calcule la date de fin de garantie en fonction de la réception et de la durée."""
    if not date_reception:
        return None
    if duree_unite == 'jour':
        return date_reception + timedelta(days=duree_valeur)
    if duree_unite == 'mois':
        return date_reception + timedelta(days=duree_valeur * 30)
    if duree_unite == 'annee':
        return date_reception + timedelta(days=duree_valeur * 365)
    return None

def build_upcoming_warranty_notifications_for_bureau() -> List[Dict]:
    """Retourne les notifications des commandes bureau expirant dans ≤ 30 jours."""
    today = datetime.now().date()
    horizon = today + timedelta(days=30)
    notifications: List[Dict] = []
    commandes = CommandeBureau.objects.select_related('fournisseur').all()
    for cmd in commandes:
        fin_garantie = calculate_garantie_end_date(cmd.date_reception, cmd.duree_garantie_valeur, cmd.duree_garantie_unite)
        if not fin_garantie:
            continue
        if today <= fin_garantie <= horizon:
            jours_restants = (fin_garantie - today).days
            
            # Déterminer l'urgence
            if jours_restants <= 7:
                urgence = 'urgente'
            elif jours_restants <= 15:
                urgence = 'attention'
            else:
                urgence = 'info'
            
            notifications.append({
                'titre': f'Garantie Bureau - {cmd.numero_commande}',
                'description': f'La garantie de la commande {cmd.numero_commande} expire bientôt',
                'details': f'Fournisseur: {cmd.fournisseur.nom if hasattr(cmd.fournisseur, "nom") else str(cmd.fournisseur)} | Type: Bureau',
                'urgence': urgence,
                'jours_restants': jours_restants,
                'timestamp': fin_garantie.strftime('%d/%m/%Y'),
                'type': 'Bureau',
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom if hasattr(cmd.fournisseur, 'nom') else str(cmd.fournisseur),
                'fin_garantie': fin_garantie,
            })
    # Trier par fin de garantie la plus proche
    notifications.sort(key=lambda x: x['fin_garantie'])
    return notifications

def build_upcoming_warranty_notifications_for_info() -> List[Dict]:
    """Retourne les notifications des commandes informatique expirant dans ≤ 30 jours."""
    today = datetime.now().date()
    horizon = today + timedelta(days=30)
    notifications: List[Dict] = []
    commandes = Commande.objects.select_related('fournisseur').all()
    for cmd in commandes:
        fin_garantie = calculate_garantie_end_date(cmd.date_reception, cmd.duree_garantie_valeur, cmd.duree_garantie_unite)
        if not fin_garantie:
            continue
        if today <= fin_garantie <= horizon:
            jours_restants = (fin_garantie - today).days
            
            # Déterminer l'urgence
            if jours_restants <= 7:
                urgence = 'urgente'
            elif jours_restants <= 15:
                urgence = 'attention'
            else:
                urgence = 'info'
            
            notifications.append({
                'titre': f'Garantie Informatique - {cmd.numero_commande}',
                'description': f'La garantie de la commande {cmd.numero_commande} expire bientôt',
                'details': f'Fournisseur: {cmd.fournisseur.nom if hasattr(cmd.fournisseur, "nom") else str(cmd.fournisseur)} | Type: Informatique',
                'urgence': urgence,
                'jours_restants': jours_restants,
                'timestamp': fin_garantie.strftime('%d/%m/%Y'),
                'type': 'Informatique',
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom if hasattr(cmd.fournisseur, 'nom') else str(cmd.fournisseur),
                'fin_garantie': fin_garantie,
            })
    notifications.sort(key=lambda x: x['fin_garantie'])
    return notifications

def get_user_dashboard_url(user):
    """Retourne l'URL du dashboard approprié selon le type d'utilisateur"""
    if user.is_superuser:
        return 'users:superadmin_dashboard'
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return 'users:gestionnaire_info_dashboard'
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return 'users:gestionnaire_bureau_dashboard'
    elif user.groups.filter(name__in=['Employé', 'Employe']).exists():
        return 'users:employe_dashboard'
    else:
        return 'users:employe_dashboard'

@login_required
def redirect_user(request):
    user = request.user
    
    # Utiliser les groupes Django par défaut
    if user.is_superuser:
        return redirect('users:superadmin_dashboard')
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return redirect('users:gestionnaire_info_dashboard')
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return redirect('users:gestionnaire_bureau_dashboard')
    elif user.groups.filter(name__in=['Employé', 'Employe']).exists():
        return redirect('users:employe_dashboard')
    else:
        return redirect('users:employe_dashboard')

@login_required
def superadmin_dashboard(request):
    # Vérifier que l'utilisateur est superadmin
    if not request.user.is_superuser:
        messages.error(request, 'Accès réservé aux super administrateurs.')
        return redirect('users:profil')
    # Superadmin reçoit toutes les notifications (Bureau + Informatique)
    notifications_bureau = build_upcoming_warranty_notifications_for_bureau()
    notifications_info = build_upcoming_warranty_notifications_for_info()
    warranty_notifications = notifications_bureau + notifications_info
    # Trier globalement par échéance
    warranty_notifications.sort(key=lambda x: x['fin_garantie'])

    # KPI dynamiques (liés à la base de données)
    try:
        total_equipements = MaterielInformatique.objects.count() + MaterielBureau.objects.count()
    except Exception:
        total_equipements = 0

    # Statistiques pour les cartes du dashboard
    try:
        from apps.users.models import CustomUser
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
    except Exception:
        total_users = 0
        active_users = 0

    try:
        # Garanties actives (qui ne sont pas expirées)
        today = timezone.now().date()
        active_warranties = 0
        
        # Compter les garanties actives pour les matériels IT
        materiels_it = MaterielInformatique.objects.all()
        for materiel in materiels_it:
            if materiel.date_fin_garantie_calculee and materiel.date_fin_garantie_calculee >= today:
                active_warranties += 1
        
        # Compter les garanties actives pour les matériels bureau
        materiels_bureau = MaterielBureau.objects.all()
        for materiel in materiels_bureau:
            if materiel.date_fin_garantie_calculee and materiel.date_fin_garantie_calculee >= today:
                active_warranties += 1
    except Exception:
        active_warranties = 0

    try:
        pending_requests = DemandeEquipement.objects.filter(statut='en_attente').count()
    except Exception:
        pending_requests = 0

    try:
        commandes_en_cours = (
            Commande.objects.filter(date_reception__isnull=True).count() +
            CommandeBureau.objects.filter(date_reception__isnull=True).count()
        )
    except Exception:
        commandes_en_cours = 0

    try:
        demandes_en_attente = DemandeEquipement.objects.filter(statut='en_attente').count()
    except Exception:
        demandes_en_attente = 0

    try:
        now = timezone.now()
        first_day = now.replace(day=1).date()
        if now.month == 12:
            next_month_first = now.replace(year=now.year + 1, month=1, day=1).date()
        else:
            next_month_first = now.replace(month=now.month + 1, day=1).date()
        livraisons_ce_mois = Livraison.objects.filter(
            date_livraison_effective__gte=first_day,
            date_livraison_effective__lt=next_month_first,
            statut_livraison='livree'
        ).count()
    except Exception:
        livraisons_ce_mois = 0

    # Données pour les graphiques - Commandes par mois
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        from django.utils import timezone
        
        # Calculer les commandes par mois pour les 7 derniers mois
        commandes_par_mois = []
        now = timezone.now()
        
        for i in range(6, -1, -1):  # 6 mois en arrière jusqu'à maintenant
            # Calculer le début et la fin du mois
            if now.month - i <= 0:
                year = now.year - 1
                month = now.month - i + 12
            else:
                year = now.year
                month = now.month - i
                
            date_debut = now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Calculer la fin du mois
            if month == 12:
                date_fin = date_debut.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
            else:
                date_fin = date_debut.replace(month=month + 1, day=1) - timedelta(days=1)
            
            # Commandes IT
            commandes_it = Commande.objects.filter(
                date_commande__gte=date_debut,
                date_commande__lte=date_fin
            ).count()
            
            # Commandes Bureau
            commandes_bureau = CommandeBureau.objects.filter(
                date_commande__gte=date_debut,
                date_commande__lte=date_fin
            ).count()
            
            commandes_par_mois.append({
                'mois': date_debut.strftime('%b'),
                'it': commandes_it,
                'bureau': commandes_bureau
            })
    except Exception as e:
        print(f"Erreur calcul commandes par mois: {e}")
        # Données par défaut si erreur
        commandes_par_mois = [
            {'mois': 'Jan', 'it': 5, 'bureau': 3},
            {'mois': 'Fév', 'it': 8, 'bureau': 6},
            {'mois': 'Mar', 'it': 12, 'bureau': 10},
            {'mois': 'Avr', 'it': 15, 'bureau': 12},
            {'mois': 'Mai', 'it': 18, 'bureau': 15},
            {'mois': 'Juin', 'it': 22, 'bureau': 18},
            {'mois': 'Juil', 'it': 25, 'bureau': 20}
        ]

    # Données pour les graphiques - Livraisons par statut
    try:
        # Statistiques des livraisons par statut
        livraisons_livrees = Livraison.objects.filter(statut_livraison='livree').count()
        livraisons_programmees = Livraison.objects.filter(statut_livraison='en_attente').count()
        livraisons_en_cours = Livraison.objects.filter(statut_livraison='en_cours').count()
        livraisons_retardees = Livraison.objects.filter(statut_livraison='retardee').count()
        total_livraisons = livraisons_livrees + livraisons_programmees + livraisons_en_cours + livraisons_retardees
    except Exception:
        livraisons_livrees = 0
        livraisons_programmees = 0
        livraisons_en_cours = 0
        livraisons_retardees = 0
        total_livraisons = 0

    # Activité récente - vraies données de la BD (triée par date)
    try:
        def make_aware_if_needed(dt):
            if isinstance(dt, datetime) and timezone.is_naive(dt):
                return timezone.make_aware(dt)
            return dt

        def to_datetime(value):
            # Supporte Date ou DateTime
            if isinstance(value, datetime):
                return make_aware_if_needed(value)
            return make_aware_if_needed(datetime.combine(value, datetime.min.time()))

        def humanize_days(delta_days: int) -> str:
            if delta_days == 0:
                return "Aujourd\'hui"
            return f"Il y a {delta_days}j"

        activite_recente = []

        now = timezone.now()

        # Dernières commandes IT
        dernieres_commandes_it = Commande.objects.order_by('-date_commande')[:2]
        for cmd in dernieres_commandes_it:
            cmd_dt = to_datetime(cmd.date_commande)
            jours = (now - cmd_dt).days
            activite_recente.append({
                'type': 'commande',
                'message': f'Nouvelle commande {cmd.numero_commande} créée',
                'utilisateur': 'Système',
                'temps': humanize_days(jours),
                'timestamp': cmd_dt,
                'couleur': 'green'
            })

        # Dernières livraisons
        dernieres_livraisons = Livraison.objects.order_by('-date_creation')[:2]
        for liv in dernieres_livraisons:
            if liv.statut_livraison == 'livree':
                liv_dt = liv.date_creation
                jours = (now - liv_dt).days
                activite_recente.append({
                    'type': 'livraison',
                    'message': f'Livraison {liv.numero_commande} terminée',
                    'utilisateur': 'Système',
                    'temps': humanize_days(jours),
                    'timestamp': liv_dt,
                    'couleur': 'green'
                })

        # Dernières demandes
        dernieres_demandes = DemandeEquipement.objects.order_by('-date_demande')[:2]
        for dem in dernieres_demandes:
            if dem.statut == 'approuvee':
                dem_dt = to_datetime(dem.date_demande)
                jours = (now - dem_dt).days
                activite_recente.append({
                    'type': 'demande',
                    'message': f'Demande {dem.id} approuvée',
                    'utilisateur': dem.demandeur.username,
                    'temps': humanize_days(jours),
                    'timestamp': dem_dt,
                    'couleur': 'blue'
                })

        # Alertes garantie récentes (issues des notifications calculées)
        if warranty_notifications:
            for notif in warranty_notifications[:2]:
                jours_restants = notif.get('jours_restants', 0)
                suffix = 'jour' if jours_restants == 1 else 'jours'
                activite_recente.append({
                    'type': 'garantie',
                    'message': f"Garantie {notif['numero_commande']} expire dans {jours_restants} {suffix}",
                    'utilisateur': 'Système',
                    'temps': "Aujourd'hui",
                    'timestamp': now,
                    'couleur': 'orange'
                })

        # Trier par timestamp décroissant et prendre les 4 plus récentes
        activite_recente = sorted(
            activite_recente,
            key=lambda x: x.get('timestamp', now),
            reverse=True
        )[:4]

    except Exception:
        # Activité par défaut si erreur
        activite_recente = [
            {
                'type': 'commande',
                'message': 'Aucune activité récente',
                'utilisateur': 'Système',
                'temps': 'Aujourd\'hui',
                'timestamp': timezone.now(),
                'couleur': 'gray'
            }
        ]

    # Données pour les graphiques - Répartition des matériels
    try:
        materiels_it_count = MaterielInformatique.objects.count()
        materiels_bureau_count = MaterielBureau.objects.count()
        chart_materials_data = {
            'labels': ['Matériels Informatiques', 'Matériels Bureautiques'],
            'data': [materiels_it_count, materiels_bureau_count],
            'colors': ['#3b82f6', '#8b5cf6']
        }
    except Exception:
        chart_materials_data = {
            'labels': ['Matériels Informatiques', 'Matériels Bureautiques'],
            'data': [0, 0],
            'colors': ['#3b82f6', '#8b5cf6']
        }

    # Données pour les graphiques - Statut des garanties
    try:
        from datetime import date
        today = date.today()
        
        # Garanties actives (non expirées)
        garanties_actives = 0
        garanties_expirees = 0
        
        # Compter les garanties actives pour les matériels IT
        for materiel in MaterielInformatique.objects.all():
            if materiel.date_fin_garantie_calculee and materiel.date_fin_garantie_calculee >= today:
                garanties_actives += 1
            else:
                garanties_expirees += 1
        
        # Compter les garanties actives pour les matériels bureau
        for materiel in MaterielBureau.objects.all():
            if materiel.date_fin_garantie_calculee and materiel.date_fin_garantie_calculee >= today:
                garanties_actives += 1
            else:
                garanties_expirees += 1
        
        chart_warranty_data = {
            'labels': ['Garanties Actives', 'Garanties Expirées'],
            'data': [garanties_actives, garanties_expirees],
            'colors': ['#10b981', '#ef4444']
        }
    except Exception:
        chart_warranty_data = {
            'labels': ['Garanties Actives', 'Garanties Expirées'],
            'data': [0, 0],
            'colors': ['#10b981', '#ef4444']
        }

    # Données récentes
    recent_materiels = list(MaterielInformatique.objects.all()[:3]) + list(MaterielBureau.objects.order_by('-date_creation')[:2])
    recent_demandes = DemandeEquipement.objects.order_by('-date_demande')[:5]
    
    context = {
        'warranty_notifications': warranty_notifications,
        'alerts_garantie_count': len(warranty_notifications),
        'total_equipements': total_equipements,
        'commandes_en_cours': commandes_en_cours,
        'demandes_en_attente': demandes_en_attente,
        'livraisons_ce_mois': livraisons_ce_mois,
        'livraisons_livrees': livraisons_livrees,
        'livraisons_programmees': livraisons_programmees,
        'livraisons_en_cours': livraisons_en_cours,
        'livraisons_retardees': livraisons_retardees,
        'total_livraisons': total_livraisons,
        'commandes_par_mois': commandes_par_mois,
        'activite_recente': activite_recente,
        # Nouvelles variables pour les cartes de statistiques
        'total_materials': total_equipements,
        'total_users': total_users,
        'active_warranties': active_warranties,
        'pending_requests': pending_requests,
        # Données pour les graphiques
        'chart_materials_data': chart_materials_data,
        'chart_warranty_data': chart_warranty_data,
        # Données récentes
        'recent_materiels': recent_materiels,
        'recent_demandes': recent_demandes,
    }

    return render(request, 'dashboards/superadmin.html', context)

@login_required
def gestionnaire_info_dashboard(request):
    """Dashboard pour le gestionnaire informatique avec vraies données"""
    
    # Importer les modèles nécessaires
    from apps.materiel_informatique.models import MaterielInformatique
    from apps.commande_informatique.models import Commande
    from apps.demande_equipement.models import DemandeEquipement
    from django.db.models import Count, Q
    from datetime import datetime, timedelta
    
    # Calculer les statistiques de base
    total_materiels_it = MaterielInformatique.objects.count()
    total_commandes = Commande.objects.count()
    
    # Calculer les garanties actives (matériels avec garantie non expirée)
    today = datetime.now().date()
    active_warranties = 0
    
    # Compter les matériels avec garantie non expirée
    for materiel in MaterielInformatique.objects.filter(commande__isnull=False):
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie and date_fin_garantie > today:
            active_warranties += 1
    
    # Calculer les demandes en attente
    pending_requests = DemandeEquipement.objects.filter(
        statut='en_attente'
    ).count()
    
    # Données pour le graphique de répartition des matériels
    materiels_par_statut = MaterielInformatique.objects.values('statut').annotate(
        count=Count('id')
    ).order_by('statut')
    
    chart_materials_data = {
        'labels': [item['statut'] for item in materiels_par_statut],
        'data': [item['count'] for item in materiels_par_statut],
        'colors': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
    }
    
    # Données pour le graphique des garanties
    # Actives vs expirées (seulement les matériels avec garantie)
    materiels_garantie_active = 0
    materiels_garantie_expiree = 0
    
    for materiel in MaterielInformatique.objects.filter(commande__isnull=False):
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie:
            if date_fin_garantie > today:
                materiels_garantie_active += 1
            else:
                materiels_garantie_expiree += 1
    
    chart_warranty_data = {
        'labels': ['Garantie Active', 'Garantie Expirée'],
        'data': [materiels_garantie_active, materiels_garantie_expiree],
        'colors': ['#10B981', '#F59E0B']
    }
    
    # Données récentes
    recent_materiels = MaterielInformatique.objects.all()[:5]
    recent_demandes = DemandeEquipement.objects.filter(
        categorie='informatique'
    ).order_by('-date_demande')[:5]
    
    # Notifications de garantie
    warranty_notifications = build_upcoming_warranty_notifications_for_info()
    
    context = {
        'total_materiels_it': total_materiels_it,
        'active_warranties': active_warranties,
        'total_commandes': total_commandes,
        'pending_requests': pending_requests,
        'chart_materials_data': chart_materials_data,
        'chart_warranty_data': chart_warranty_data,
        'recent_materiels': recent_materiels,
        'recent_demandes': recent_demandes,
        'warranty_notifications': warranty_notifications,
    }
    
    return render(request, 'dashboards/gestionnaire_info.html', context)

@login_required
def gestionnaire_bureau_dashboard(request):
    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import timedelta
    from apps.materiel_bureautique.models import MaterielBureau
    from apps.commande_bureau.models import CommandeBureau
    from apps.demande_equipement.models import DemandeEquipement
    
    # Date pour les comparaisons (mois dernier)
    now = timezone.now()
    last_month = now - timedelta(days=30)
    
    # Statistiques principales
    total_materiels_bureau = MaterielBureau.objects.count()
    total_commandes = CommandeBureau.objects.count()
    pending_requests = DemandeEquipement.objects.filter(
        statut='en_attente',
        categorie='bureau'
    ).count()
    
    # Garanties actives (matériels avec garantie non expirée)
    active_warranties = 0
    materiels_avec_garantie = MaterielBureau.objects.all()
    for materiel in materiels_avec_garantie:
        if materiel.date_fin_garantie_calculee and materiel.date_fin_garantie_calculee > now.date():
            active_warranties += 1
    
    # Calculs des pourcentages (comparaison avec le mois dernier)
    materiels_mois_dernier = MaterielBureau.objects.filter(
        date_creation__lt=last_month
    ).count()
    materiels_actuels = MaterielBureau.objects.count()
    pourcentage_materiels = 0
    if materiels_mois_dernier > 0:
        pourcentage_materiels = round(((materiels_actuels - materiels_mois_dernier) / materiels_mois_dernier) * 100)
    
    commandes_mois_dernier = CommandeBureau.objects.filter(
        date_commande__lt=last_month
    ).count()
    commandes_actuelles = CommandeBureau.objects.count()
    pourcentage_commandes = 0
    if commandes_mois_dernier > 0:
        pourcentage_commandes = round(((commandes_actuelles - commandes_mois_dernier) / commandes_mois_dernier) * 100)
    
    demandes_mois_dernier = DemandeEquipement.objects.filter(
        date_demande__lt=last_month,
        categorie='bureau'
    ).count()
    demandes_actuelles = DemandeEquipement.objects.filter(categorie='bureau').count()
    pourcentage_demandes = 0
    if demandes_mois_dernier > 0:
        pourcentage_demandes = round(((demandes_actuelles - demandes_mois_dernier) / demandes_mois_dernier) * 100)
    
    # Données pour le graphique de répartition des matériels
    repartition_materiels = MaterielBureau.objects.values('statut').annotate(
        count=Count('id')
    ).order_by('statut')
    
    chart_materials_data = {
        'labels': [item['statut'] for item in repartition_materiels],
        'data': [item['count'] for item in repartition_materiels],
        'colors': ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']
    }
    
    # Données pour le graphique des garanties
    garanties_actives = 0
    garanties_expirees = 0
    garanties_expirant_soon = 0
    
    for materiel in MaterielBureau.objects.all():
        if materiel.date_fin_garantie_calculee:
            if materiel.date_fin_garantie_calculee > now.date():
                garanties_actives += 1
                # Vérifier si la garantie expire dans les 30 prochains jours
                if materiel.date_fin_garantie_calculee <= (now.date() + timedelta(days=30)):
                    garanties_expirant_soon += 1
            else:
                garanties_expirees += 1
    
    chart_warranty_data = {
        'labels': ['Actives', 'Expirées', 'Expirant bientôt'],
        'data': [garanties_actives, garanties_expirees, garanties_expirant_soon],
        'colors': ['#10b981', '#ef4444', '#f59e0b']
    }
    
    # Données récentes
    recent_materiels = MaterielBureau.objects.order_by('-date_creation')[:5]
    recent_demandes = DemandeEquipement.objects.filter(
        categorie='bureau'
    ).order_by('-date_demande')[:5]
    
    warranty_notifications = build_upcoming_warranty_notifications_for_bureau()
    
    return render(request, 'dashboards/gestionnaire_bureau.html', {
        'total_materiels_bureau': total_materiels_bureau,
        'active_warranties': active_warranties,
        'total_commandes': total_commandes,
        'pending_requests': pending_requests,
        'pourcentage_materiels': pourcentage_materiels,
        'pourcentage_commandes': pourcentage_commandes,
        'pourcentage_demandes': pourcentage_demandes,
        'chart_materials_data': chart_materials_data,
        'chart_warranty_data': chart_warranty_data,
        'recent_materiels': recent_materiels,
        'recent_demandes': recent_demandes,
        'warranty_notifications': warranty_notifications,
    })

@login_required
def employe_dashboard(request):
    user = request.user
    
    # Statistiques dynamiques pour l'employé
    try:
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.materiel_bureautique.models import MaterielBureau
        from apps.demande_equipement.models import DemandeEquipement
        
        # Compter les équipements attribués à cet employé
        equipements_it_count = MaterielInformatique.objects.filter(
            utilisateur=user, 
            statut='affecte'
        ).count()
        
        equipements_bureau_count = MaterielBureau.objects.filter(
            utilisateur=user, 
            statut='affecte'
        ).count()
        
        # Compter les demandes en cours de cet employé
        demandes_count = DemandeEquipement.objects.filter(
            demandeur=user,
            statut__in=['en_attente', 'en_cours', 'approuvee']
        ).count()
        
        # Données pour le graphique - répartition par type d'équipement
        from django.db.models import Count
        
        # Équipements IT par statut
        equipements_it_par_statut = MaterielInformatique.objects.filter(
            utilisateur=user
        ).values('statut').annotate(
            count=Count('id')
        ).order_by('statut')
        
        # Équipements Bureau par statut
        equipements_bureau_par_statut = MaterielBureau.objects.filter(
            utilisateur=user
        ).values('statut').annotate(
            count=Count('id')
        ).order_by('statut')
        
        # Préparer les données pour Chart.js - graphique en donut
        chart_labels = []
        chart_data = []
        chart_colors = []
        
        # Ajouter les équipements IT
        for statut_data in equipements_it_par_statut:
            if statut_data['count'] > 0:
                chart_labels.append(f"IT - {statut_data['statut']}")
                chart_data.append(statut_data['count'])
                chart_colors.append('#3b82f6')  # Bleu pour IT
        
        # Ajouter les équipements Bureau
        for statut_data in equipements_bureau_par_statut:
            if statut_data['count'] > 0:
                chart_labels.append(f"Bureau - {statut_data['statut']}")
                chart_data.append(statut_data['count'])
                chart_colors.append('#8b5cf6')  # Violet pour Bureau
        
        # Si pas de données, créer des données par défaut
        if not chart_data:
            chart_labels = ['Aucun équipement']
            chart_data = [1]
            chart_colors = ['#9ca3af']
        
        # Ajouter des informations sur les équipements récents
        equipements_it_recents = MaterielInformatique.objects.filter(
            utilisateur=user
        ).order_by('-id')[:5]
        
        equipements_bureau_recents = MaterielBureau.objects.filter(
            utilisateur=user
        ).order_by('-id')[:5]
        
        # Demandes récentes
        demandes_recentes = DemandeEquipement.objects.filter(
            demandeur=user
        ).order_by('-date_demande')[:5]
        
        # Statistiques supplémentaires
        total_equipements = equipements_it_count + equipements_bureau_count
        equipements_en_panne = MaterielInformatique.objects.filter(
            utilisateur=user, 
            statut='en panne'
        ).count() + MaterielBureau.objects.filter(
            utilisateur=user, 
            statut='Réparation'
        ).count()
        
    except Exception as e:
        # En cas d'erreur, utiliser des valeurs par défaut et logger l'erreur
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur dans employe_dashboard pour l'utilisateur {user.username}: {e}")
        
        equipements_it_count = 0
        equipements_bureau_count = 0
        demandes_count = 0
        total_equipements = 0
        equipements_en_panne = 0
        chart_labels = ['Aucun équipement']
        chart_data = [1]
        chart_colors = ['#9ca3af']
        equipements_it_recents = []
        equipements_bureau_recents = []
        demandes_recentes = []
    
    import json
    
    context = {
        'equipements_it_count': equipements_it_count,
        'equipements_bureau_count': equipements_bureau_count,
        'demandes_count': demandes_count,
        'total_equipements': total_equipements,
        'equipements_en_panne': equipements_en_panne,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'chart_colors': json.dumps(chart_colors),
        'equipements_it_recents': equipements_it_recents,
        'equipements_bureau_recents': equipements_bureau_recents,
        'demandes_recentes': demandes_recentes,
        'debug': settings.DEBUG,
    }
    
    return render(request, 'dashboards/employe.html', context)

def custom_logout_view(request):
    logout(request)
    return redirect('/accounts/login/')  # Redirection vers la page de login Django

@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})

@login_required
def profil(request):
    """Vue du profil utilisateur"""
    user = request.user
    
    # Calculer les vraies statistiques
    stats = {}
    
    if user.groups.filter(name='Gestionnaire Informatique').exists():
        # Statistiques pour le gestionnaire informatique
        try:
            from apps.materiel_informatique.models import MaterielInformatique
            from apps.commande_informatique.models import Commande
            from apps.livraison.models import Livraison
            
            stats['equipements_geres'] = MaterielInformatique.objects.count()
            stats['commandes_traitees'] = Commande.objects.count()
            stats['livraisons_suivies'] = Livraison.objects.filter(type_commande='informatique').count()
        except ImportError:
            stats['equipements_geres'] = 0
            stats['commandes_traitees'] = 0
            stats['livraisons_suivies'] = 0
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        # Statistiques pour le gestionnaire bureau
        try:
            from apps.materiel_bureautique.models import MaterielBureau
            from apps.commande_bureau.models import CommandeBureau
            from apps.livraison.models import Livraison
            
            stats['equipements_geres'] = MaterielBureau.objects.count()
            stats['commandes_traitees'] = CommandeBureau.objects.count()
            stats['livraisons_suivies'] = Livraison.objects.filter(type_commande='bureau').count()
        except ImportError:
            stats['equipements_geres'] = 0
            stats['commandes_traitees'] = 0
            stats['livraisons_suivies'] = 0
    else:
        # Statistiques par défaut
        stats['equipements_geres'] = 0
        stats['commandes_traitees'] = 0
        stats['livraisons_suivies'] = 0
    
    context = {
        'user': user,
        'stats': stats
    }
    
    if user.is_superuser:
        return render(request, 'users/profile_superadmin.html', context)
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return render(request, 'users/profile_gestionnaire_info.html', context)
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return render(request, 'users/profile_gestionnaire_bureau.html', context)
    else:
        return render(request, 'users/profile.html', context)

@login_required
def dashboard_garantie(request):
    """Redirection vers le dashboard de garantie Streamlit"""
    # Vérifier les permissions de l'utilisateur
    user = request.user
    
    # Seuls les Super Admin, Gestionnaire Informatique et Gestionnaire Bureau peuvent accéder
    if not (user.is_superuser or 
            user.groups.filter(name='Gestionnaire Informatique').exists() or 
            user.groups.filter(name='Gestionnaire Bureau').exists()):
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires pour accéder au Dashboard de Garanties.')
        return redirect('users:profil')
    
    try:
        # Essayer d'abord le dashboard complet (8502), puis secours sur 8501
        candidate_bases = ['http://localhost:8502', 'http://localhost:8501']

        for base_url in candidate_bases:
            try:
                response = requests.get(base_url, timeout=4)
            except requests.exceptions.RequestException:
                continue

            if response.status_code == 200:
                username = request.user.username
                import urllib.parse
                encoded_username = urllib.parse.quote(username)
                streamlit_url = f"{base_url}/?username={encoded_username}"
                logger.info(
                    f"Redirection vers Streamlit {base_url} avec utilisateur: {username} (encodé: {encoded_username})"
                )
                return redirect(streamlit_url)

        # Si aucun dashboard n'est accessible, afficher un message d'erreur
        messages.error(request, 'Le Dashboard de Garanties n\'est pas accessible actuellement. Veuillez réessayer plus tard.')
        return redirect('users:profil')

    except Exception as e:
        logger.error(f"Erreur lors de l'accès au dashboard de garantie: {e}")
        messages.error(request, 'Erreur lors de l\'accès au Dashboard de Garanties.')
        return redirect('users:profil')

@login_required
def superadmin_dashboard_debug(request):
    """Vue de test pour déboguer les graphiques du dashboard superadmin"""
    if not request.user.is_superuser:
        messages.error(request, 'Accès réservé aux super administrateurs.')
        return redirect('users:profil')
    
    # Récupérer les mêmes données que la vue principale
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count
        from django.utils import timezone
        
        # KPI dynamiques
        total_equipements = MaterielInformatique.objects.count() + MaterielBureau.objects.count()
        commandes_en_cours = (
            Commande.objects.filter(date_reception__isnull=True).count() +
            CommandeBureau.objects.filter(date_reception__isnull=True).count()
        )
        demandes_en_attente = DemandeEquipement.objects.filter(statut='en_attente').count()
        
        # Données pour les graphiques - Commandes par mois
        commandes_par_mois = []
        now = timezone.now()
        
        for i in range(6, -1, -1):  # 6 mois en arrière jusqu'à maintenant
            if now.month - i <= 0:
                year = now.year - 1
                month = now.month - i + 12
            else:
                year = now.year
                month = now.month - i
                
            date_debut = now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if month == 12:
                date_fin = date_debut.replace(year=year + 1, month=1, day=1) - timedelta(days=1)
            else:
                date_fin = date_debut.replace(month=month + 1, day=1) - timedelta(days=1)
            
            commandes_it = Commande.objects.filter(
                date_commande__gte=date_debut,
                date_commande__lte=date_fin
            ).count()
            
            commandes_bureau = CommandeBureau.objects.filter(
                date_commande__gte=date_debut,
                date_commande__lte=date_fin
            ).count()
            
            commandes_par_mois.append({
                'mois': date_debut.strftime('%b'),
                'it': commandes_it,
                'bureau': commandes_bureau
            })
        
        # Données pour les graphiques - Livraisons par statut
        livraisons_livrees = Livraison.objects.filter(statut_livraison='livree').count()
        livraisons_programmees = Livraison.objects.filter(statut_livraison='en_attente').count()
        livraisons_en_cours = Livraison.objects.filter(statut_livraison='en_cours').count()
        livraisons_retardees = Livraison.objects.filter(statut_livraison='retardee').count()
        
        context = {
            'total_equipements': total_equipements,
            'commandes_en_cours': commandes_en_cours,
            'demandes_en_attente': demandes_en_attente,
            'commandes_par_mois': commandes_par_mois,
            'livraisons_livrees': livraisons_livrees,
            'livraisons_programmees': livraisons_programmees,
            'livraisons_en_cours': livraisons_en_cours,
            'livraisons_retardees': livraisons_retardees,
        }
        
    except Exception as e:
        print(f"Erreur dans la vue debug: {e}")
        context = {
            'total_equipements': 0,
            'commandes_en_cours': 0,
            'demandes_en_attente': 0,
            'commandes_par_mois': [],
            'livraisons_livrees': 0,
            'livraisons_programmees': 0,
            'livraisons_en_cours': 0,
            'livraisons_retardees': 0,
        }
    
    return render(request, 'dashboards/superadmin_debug.html', context)

@require_http_methods(["POST"])
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

def global_search(request):
    """Vue pour la recherche globale du superadmin"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = []
    
    # Recherche dans les équipements informatiques
    if MaterielInformatique:
        equipements_it = MaterielInformatique.objects.filter(
            Q(numero_serie__icontains=query) | 
            Q(code_inventaire__icontains=query) |
            Q(statut__icontains=query)
        )[:5]
        
        for equip in equipements_it:
            results.append({
                'type': 'equipement',
                'title': f"Équipement IT - {equip.code_inventaire}",
                'subtitle': f"Série: {equip.numero_serie} - Statut: {equip.statut}",
                'url': reverse('materiel_informatique:liste_materiels'),
                'icon': 'computer'
            })
    
    # Recherche dans les équipements bureautiques
    if MaterielBureau:
        equipements_bureau = MaterielBureau.objects.filter(
            Q(code_inventaire__icontains=query) |
            Q(statut__icontains=query)
        )[:5]
        
        for equip in equipements_bureau:
            results.append({
                'type': 'equipement',
                'title': f"Équipement Bureau - {equip.code_inventaire}",
                'subtitle': f"{equip.designation} - Statut: {equip.statut}",
                'url': reverse('materiel_bureautique:liste_materiels'),
                'icon': 'book'
            })
    
    # Recherche dans les commandes informatiques
    if Commande:
        commandes_it = Commande.objects.filter(
            Q(numero_commande__icontains=query) |
            Q(mode_passation__icontains=query)
        )[:5]
        
        for cmd in commandes_it:
            results.append({
                'type': 'commande',
                'title': f"Commande IT #{cmd.numero_commande}",
                'subtitle': f"{cmd.mode_passation} - {cmd.fournisseur.nom}",
                'url': reverse('commandes_informatique:liste_commandes'),
                'icon': 'shopping-cart'
            })
    
    # Recherche dans les commandes bureau
    if CommandeBureau:
        commandes_bureau = CommandeBureau.objects.filter(
            Q(numero_commande__icontains=query) |
            Q(mode_passation__icontains=query)
        )[:5]
        
        for cmd in commandes_bureau:
            results.append({
                'type': 'commande',
                'title': f"Commande Bureau #{cmd.numero_commande}",
                'subtitle': f"{cmd.mode_passation} - {cmd.fournisseur.nom}",
                'url': reverse('commandes_bureau:liste_commandes'),
                'icon': 'document'
            })
    
    # Recherche dans les fournisseurs
    if Fournisseur:
        fournisseurs = Fournisseur.objects.filter(
            Q(nom__icontains=query) |
            Q(if_fiscal__icontains=query) |
            Q(ice__icontains=query)
        )[:5]
        
        for fourn in fournisseurs:
            results.append({
                'type': 'fournisseur',
                'title': fourn.nom,
                'subtitle': f"IF: {fourn.if_fiscal}" if fourn.if_fiscal else "IF non renseigné",
                'url': reverse('fournisseurs:fournisseur_list'),
                'icon': 'building'
            })
    
    # Recherche dans les demandes
    if DemandeEquipement:
        demandes = DemandeEquipement.objects.filter(
            Q(categorie__icontains=query) |
            Q(type_demande__icontains=query) |
            Q(statut__icontains=query)
        )[:5]
        
        for dem in demandes:
            # Déterminer la description selon la catégorie
            if dem.categorie == 'informatique' and dem.designation_info:
                description = dem.designation_info.nom
            elif dem.categorie == 'bureau' and dem.designation_bureau:
                description = dem.designation_bureau.nom
            elif dem.fourniture:
                description = dem.fourniture.nom
            else:
                description = f"Demande {dem.type_demande}"
                
            results.append({
                'type': 'demande',
                'title': f"Demande: {description}",
                'subtitle': f"Par {dem.demandeur.get_full_name()} - {dem.get_statut_display()}",
                'url': reverse('demande_equipement:liste_toutes_demandes'),
                'icon': 'document-text'
            })
    
    return JsonResponse({'results': results[:10]})  # Limiter à 10 résultats

@login_required
def notifications_garantie(request):
    """
    Récupère les notifications de garantie expirante selon le rôle de l'utilisateur
    """
    user = request.user
    notifications = []
    
    # Date limite : 1 mois à partir d'aujourd'hui
    date_limite = timezone.now().date() + timedelta(days=30)
    
    if user.is_superuser or user.groups.filter(name='Super Admin').exists():
        # Super Admin : voir toutes les commandes avec garantie expirante
        notifications.extend(get_notifications_materiel_info(date_limite))
        notifications.extend(get_notifications_materiel_bureau(date_limite))
        
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        # Gestionnaire Info : seulement matériel informatique
        notifications.extend(get_notifications_materiel_info(date_limite))
        
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        # Gestionnaire Bureau : seulement matériel bureau
        notifications.extend(get_notifications_materiel_bureau(date_limite))
    
    return JsonResponse({'notifications': notifications})

def get_notifications_materiel_info(date_limite):
    """Récupère les notifications pour le matériel informatique"""
    notifications = []
    
    materiels = MaterielInformatique.objects.select_related(
        'ligne_commande__commande__fournisseur',
        'utilisateur'
    ).all()
    
    for materiel in materiels:
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie and date_fin_garantie <= date_limite:
            jours_restants = (date_fin_garantie - timezone.now().date()).days
            
            notification = {
                'type': 'informatique',
                'materiel_id': materiel.id,
                'code_inventaire': materiel.code_inventaire,
                'numero_serie': materiel.numero_serie,
                'designation': materiel.ligne_commande.designation.nom,
                'description': materiel.ligne_commande.description.nom,
                'fournisseur': materiel.ligne_commande.commande.fournisseur.nom,
                'numero_commande': materiel.ligne_commande.commande.numero_commande,
                'date_fin_garantie': date_fin_garantie.strftime('%d/%m/%Y'),
                'jours_restants': jours_restants,
                'utilisateur': materiel.utilisateur.username if materiel.utilisateur else 'Non affecté',
                'statut': materiel.statut,
                'urgence': 'critique' if jours_restants <= 7 else 'warning' if jours_restants <= 15 else 'info'
            }
            notifications.append(notification)
    
    return notifications

def get_notifications_materiel_bureau(date_limite):
    """Récupère les notifications pour le matériel bureau"""
    notifications = []
    
    materiels = MaterielBureau.objects.select_related(
        'ligne_commande__commande__fournisseur',
        'utilisateur'
    ).all()
    
    for materiel in materiels:
        date_fin_garantie = materiel.date_fin_garantie_calculee
        if date_fin_garantie and date_fin_garantie <= date_limite:
            jours_restants = (date_fin_garantie - timezone.now().date()).days
            
            notification = {
                'type': 'bureau',
                'materiel_id': materiel.id,
                'code_inventaire': materiel.code_inventaire,
                'designation': materiel.ligne_commande.designation.nom,
                'description': materiel.ligne_commande.description.nom,
                'fournisseur': materiel.ligne_commande.commande.fournisseur.nom,
                'numero_commande': materiel.ligne_commande.commande.numero_commande,
                'date_fin_garantie': date_fin_garantie.strftime('%d/%m/%Y'),
                'jours_restants': jours_restants,
                'utilisateur': materiel.utilisateur.username if materiel.utilisateur else 'Non affecté',
                'statut': materiel.statut,
                'urgence': 'critique' if jours_restants <= 7 else 'warning' if jours_restants <= 15 else 'info'
            }
            notifications.append(notification)
    
    return notifications