from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict

from apps.commande_bureau.models import CommandeBureau
from apps.commande_informatique.models import Commande

logger = logging.getLogger(__name__)

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
            notifications.append({
                'type': 'Bureau',
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom if hasattr(cmd.fournisseur, 'nom') else str(cmd.fournisseur),
                'fin_garantie': fin_garantie,
                'jours_restants': (fin_garantie - today).days,
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
            notifications.append({
                'type': 'Informatique',
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom if hasattr(cmd.fournisseur, 'nom') else str(cmd.fournisseur),
                'fin_garantie': fin_garantie,
                'jours_restants': (fin_garantie - today).days,
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
    else:
        return redirect('users:employe_dashboard')

@login_required
def superadmin_dashboard(request):
    # Superadmin reçoit toutes les notifications (Bureau + Informatique)
    notifications_bureau = build_upcoming_warranty_notifications_for_bureau()
    notifications_info = build_upcoming_warranty_notifications_for_info()
    warranty_notifications = notifications_bureau + notifications_info
    # Trier globalement par échéance
    warranty_notifications.sort(key=lambda x: x['fin_garantie'])
    return render(request, 'dashboards/superadmin.html', {
        'warranty_notifications': warranty_notifications,
    })

@login_required
def gestionnaire_info_dashboard(request):
    warranty_notifications = build_upcoming_warranty_notifications_for_info()
    return render(request, 'dashboards/gestionnaire_info.html', {
        'warranty_notifications': warranty_notifications,
    })

@login_required
def gestionnaire_bureau_dashboard(request):
    warranty_notifications = build_upcoming_warranty_notifications_for_bureau()
    return render(request, 'dashboards/gestionnaire_bureau.html', {
        'warranty_notifications': warranty_notifications,
    })

@login_required
def employe_dashboard(request):
    return render(request, 'dashboards/employe.html')

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Make sure you have a 'login' URL name defined

@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})

@login_required
def profil(request):
    """Vue du profil utilisateur"""
    return render(request, 'users/profile.html')

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

        messages.error(request, "Le dashboard de garantie n'est pas accessible sur 8502/8501. Veuillez le démarrer.")
        return redirect('users:profil')

    except Exception as e:
        logger.warning(f"Erreur lors de la redirection dashboard garantie: {e}")
        messages.warning(
            request,
            "Impossible d'accéder au dashboard de garantie. Lancez-le avec: ./dashboard_garantie/start_dashboard.sh"
        )
        return redirect('users:profil')

@require_http_methods(["POST"])
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')