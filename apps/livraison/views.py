from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Livraison
from .forms import LivraisonForm, RechercheLivraisonForm, NouvelleLivraisonForm

User = get_user_model()


@login_required
def liste_livraisons(request):
    """Affiche le tableau des livraisons avec toutes les commandes"""
    
    # Récupérer toutes les livraisons avec optimisations
    livraisons = Livraison.objects.select_related(
        'commande_informatique__fournisseur',
        'commande_bureau__fournisseur',
        'cree_par'
    ).prefetch_related(
        'commande_informatique__lignes__designation',
        'commande_informatique__lignes__description',
        'commande_bureau__lignes__designation',
        'commande_bureau__lignes__description'
    ).all()
    
    # Filtrage selon le type d'utilisateur
    user = request.user
    if user.is_superuser:
        # Superadmin voit tout
        pass
    elif hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique:
        # Gestionnaire informatique voit seulement les commandes informatique
        livraisons = livraisons.filter(type_commande='informatique')
    elif hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau:
        # Gestionnaire bureau voit seulement les commandes bureau
        livraisons = livraisons.filter(type_commande='bureau')
    else:
        # Utilisateurs normaux ne voient rien
        livraisons = Livraison.objects.none()
    
    # Filtres
    form = RechercheLivraisonForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        type_commande = form.cleaned_data.get('type_commande')
        statut_livraison = form.cleaned_data.get('statut_livraison')
        conforme = form.cleaned_data.get('conforme')
        pv_reception = form.cleaned_data.get('pv_reception')
        
        if search:
            livraisons = livraisons.filter(
                Q(numero_commande__icontains=search) |
                Q(commande_informatique__fournisseur__nom__icontains=search) |
                Q(commande_bureau__fournisseur__nom__icontains=search) |
                Q(notes__icontains=search)
            )
        
        if type_commande:
            livraisons = livraisons.filter(type_commande=type_commande)
        
        if statut_livraison:
            livraisons = livraisons.filter(statut_livraison=statut_livraison)
        
        if conforme and conforme in ['True', 'False']:
            livraisons = livraisons.filter(conforme=conforme == 'True')
        
        if pv_reception and pv_reception in ['True', 'False']:
            livraisons = livraisons.filter(pv_reception_recu=pv_reception == 'True')
    
    # Pagination
    paginator = Paginator(livraisons, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    total_livraisons = livraisons.count()
    livraisons_livrees = livraisons.filter(statut_livraison='livree').count()
    livraisons_conformes = livraisons.filter(conforme=True).count()
    pv_recus = livraisons.filter(pv_reception_recu=True).count()
    
    # Déterminer le dashboard approprié selon le type d'utilisateur
    dashboard_url = ''
    if user.is_superuser:
        dashboard_url = 'users:superadmin_dashboard'
    elif hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique:
        dashboard_url = 'users:gestionnaire_info_dashboard'
    elif hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau:
        dashboard_url = 'users:gestionnaire_bureau_dashboard'
    else:
        dashboard_url = 'users:employe_dashboard'
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_livraisons': total_livraisons,
        'livraisons_livrees': livraisons_livrees,
        'livraisons_conformes': livraisons_conformes,
        'pv_recus': pv_recus,
        'dashboard_url': dashboard_url,
    }
    
    return render(request, 'livraison/liste_livraisons.html', context)


@login_required
def detail_livraison(request, pk):
    """Détail d'une livraison avec les matériels"""
    livraison = get_object_or_404(Livraison.objects.select_related(
        'commande_informatique__fournisseur',
        'commande_bureau__fournisseur',
        'cree_par',
        'modifie_par'
    ).prefetch_related(
        'commande_informatique__lignes__designation',
        'commande_informatique__lignes__description',
        'commande_bureau__lignes__designation',
        'commande_bureau__lignes__description'
    ), pk=pk)
    
    # Vérifier les permissions
    user = request.user
    if not user.is_superuser:
        if livraison.type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
        elif livraison.type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
    
    # Calculer le total pour chaque matériel
    materiels_avec_total = []
    for materiel in livraison.materiels:
        materiel.total = materiel.prix_unitaire * materiel.quantite
        materiels_avec_total.append(materiel)
    
    context = {
        'livraison': livraison,
        'materiels': materiels_avec_total,
    }
    return render(request, 'livraison/detail_livraison.html', context)


@login_required
def nouvelle_livraison(request):
    """Créer une nouvelle livraison avec formulaire personnalisé"""
    user = request.user
    
    # Vérifier les permissions
    if not user.is_superuser and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique) and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
        messages.error(request, "Vous n'avez pas les permissions pour créer une livraison.")
        return redirect('livraison:liste_livraisons')
    
    # Déterminer le type de commande selon l'utilisateur
    type_commande_initial = ''
    if user.is_superuser:
        type_commande_initial = ''
    elif hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique:
        type_commande_initial = 'informatique'
    elif hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau:
        type_commande_initial = 'bureau'
    
    if request.method == 'POST':
        form = NouvelleLivraisonForm(request.POST)
        if form.is_valid():
            # Traitement du formulaire
            commande_id = form.cleaned_data['commande_id']
            type_commande = form.cleaned_data['type_commande']
            date_livraison_prevue = form.cleaned_data['date_livraison_prevue']
            date_livraison_effective = form.cleaned_data['date_livraison_effective']
            statut_livraison = form.cleaned_data['statut_livraison']
            conforme = form.cleaned_data['conforme']
            pv_reception_recu = form.cleaned_data['pv_reception_recu']
            notes = form.cleaned_data['notes']
        
            # Utiliser le type de commande sélectionné dans le formulaire
            if type_commande == 'informatique':
                from apps.commande_informatique.models import Commande as CommandeInfo
                try:
                    commande_informatique = CommandeInfo.objects.get(id=commande_id)
                    commande_bureau = None
                except CommandeInfo.DoesNotExist:
                    messages.error(request, "Commande informatique introuvable.")
                    return redirect('livraison:nouvelle_livraison')
            elif type_commande == 'bureau':
                from apps.commande_bureau.models import CommandeBureau
                try:
                    commande_bureau = CommandeBureau.objects.get(id=commande_id)
                    commande_informatique = None
                except CommandeBureau.DoesNotExist:
                    messages.error(request, "Commande bureau introuvable.")
                    return redirect('livraison:nouvelle_livraison')
            else:
                messages.error(request, "Type de commande invalide.")
                return redirect('livraison:nouvelle_livraison')
            
            # Vérifier si une livraison existe déjà pour cette commande
            numero_commande = commande_informatique.numero_commande if commande_informatique else commande_bureau.numero_commande
            
            print(f"DEBUG - Vérification: numero_commande={numero_commande}, type_commande={type_commande}")
            
            livraison_existante = Livraison.objects.filter(numero_commande=numero_commande, type_commande=type_commande).first()
            if livraison_existante:
                print(f"DEBUG - Livraison existante trouvée: {livraison_existante}")
                messages.error(request, f'Une livraison existe déjà pour la commande {numero_commande}.')
                return redirect('livraison:detail_livraison', pk=livraison_existante.pk)
            else:
                print(f"DEBUG - Aucune livraison existante trouvée")
            
            # Créer la livraison
            print(f"DEBUG - Tentative de création: numero_commande={numero_commande}, type_commande={type_commande}")
            try:
                livraison = Livraison.objects.create(
                    numero_commande=numero_commande,
                    type_commande=type_commande,
                    commande_informatique=commande_informatique,
                    commande_bureau=commande_bureau,
                    date_livraison_prevue=date_livraison_prevue,
                    date_livraison_effective=date_livraison_effective or None,
                    statut_livraison=statut_livraison,
                    conforme=conforme,
                    pv_reception_recu=pv_reception_recu,
                    notes=notes,
                    cree_par=user
                )
                
                print(f"DEBUG - Livraison créée avec succès: {livraison}")
                messages.success(request, f'Livraison pour la commande {livraison.numero_commande} créée avec succès.')
                return redirect('livraison:detail_livraison', pk=livraison.pk)
            except Exception as e:
                print(f"DEBUG - Erreur lors de la création: {str(e)}")
                messages.error(request, f'Erreur lors de la création de la livraison : {str(e)}')
                return redirect('livraison:nouvelle_livraison')
        else:
            # Formulaire invalide - afficher les erreurs
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        # GET request - afficher le formulaire
        form = NouvelleLivraisonForm(initial={'type_commande': type_commande_initial})
    
    context = {
        'form': form,
        'type_commande_initial': type_commande_initial
    }
    return render(request, 'livraison/form_livraison.html', context)


@login_required
def modifier_livraison(request, pk):
    """Modifier une livraison"""
    livraison = get_object_or_404(Livraison, pk=pk)
    
    # Vérifier les permissions
    user = request.user
    if not user.is_superuser:
        if livraison.type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
        elif livraison.type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
    
    if request.method == 'POST':
        from .forms import ModifierLivraisonForm
        form = ModifierLivraisonForm(request.POST)
        
        if form.is_valid():
            # Mettre à jour la livraison avec les données du formulaire
            livraison.date_livraison_prevue = form.cleaned_data['date_livraison_prevue']
            livraison.date_livraison_effective = form.cleaned_data['date_livraison_effective'] or None
            livraison.statut_livraison = form.cleaned_data['statut_livraison']
            livraison.conforme = form.cleaned_data['conforme']
            livraison.pv_reception_recu = form.cleaned_data['pv_reception_recu']
            livraison.notes = form.cleaned_data['notes']
            livraison.modifie_par = user
            livraison.save()
            
            messages.success(request, f'Livraison {livraison.numero_commande} modifiée avec succès.')
            return redirect('livraison:detail_livraison', pk=livraison.pk)
        else:
            # Afficher les erreurs spécifiques pour le debug
            print("DEBUG - Erreurs de formulaire:", form.errors)
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        # Pré-remplir le formulaire avec les données existantes
        from .forms import ModifierLivraisonForm
        initial_data = {
            'type_commande': livraison.type_commande,
            'commande_id': livraison.commande_informatique.id if livraison.commande_informatique else livraison.commande_bureau.id,
            'date_livraison_prevue': livraison.date_livraison_prevue.strftime('%Y-%m-%d') if livraison.date_livraison_prevue else None,
            'date_livraison_effective': livraison.date_livraison_effective.strftime('%Y-%m-%d') if livraison.date_livraison_effective else None,
            'statut_livraison': livraison.statut_livraison,
            'conforme': livraison.conforme,
            'pv_reception_recu': livraison.pv_reception_recu,
            'notes': livraison.notes,
        }
        
        # Debug: afficher les valeurs initiales
        print("DEBUG - Valeurs initiales:", initial_data)
        
        form = ModifierLivraisonForm(initial=initial_data)
    
    # Calculer le total pour chaque matériel (comme dans detail_livraison)
    materiels_avec_total = []
    for materiel in livraison.materiels:
        materiel.total = materiel.prix_unitaire * materiel.quantite
        materiels_avec_total.append(materiel)
    
    context = {
        'form': form,
        'livraison': livraison,
        'materiels': materiels_avec_total,  # Passer les matériels avec total calculé
        'titre': f'Modifier la livraison {livraison.numero_commande}',
        'is_edit': True  # Flag pour indiquer qu'on est en mode modification
    }
    return render(request, 'livraison/form_livraison.html', context)


@login_required
def supprimer_livraison(request, pk):
    """Supprimer une livraison"""
    livraison = get_object_or_404(Livraison, pk=pk)
    
    # Vérifier les permissions
    user = request.user
    if not user.is_superuser:
        if livraison.type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
        elif livraison.type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
    
    if request.method == 'POST':
        numero = livraison.numero_commande
        livraison.delete()
        messages.success(request, f'Livraison {numero} supprimée avec succès.')
        return redirect('livraison:liste_livraisons')
    
    context = {
        'livraison': livraison
    }
    return render(request, 'livraison/confirmer_suppression.html', context)


@login_required
def marquer_livree(request, pk):
    """Marquer une livraison comme livrée"""
    livraison = get_object_or_404(Livraison, pk=pk)
    
    # Vérifier les permissions
    user = request.user
    if not user.is_superuser:
        if livraison.type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
        elif livraison.type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
    
    if request.method == 'POST':
        livraison.statut_livraison = 'livree'
        livraison.modifie_par = user
        livraison.save()
        
        messages.success(request, f'Livraison {livraison.numero_commande} marquée comme livrée.')
        return redirect('livraison:detail_livraison', pk=pk)
    
    context = {
        'livraison': livraison
    }
    return render(request, 'livraison/marquer_livree.html', context)


@login_required
def valider_pv_reception(request, pk):
    """Valider le PV de réception"""
    livraison = get_object_or_404(Livraison, pk=pk)
    
    # Vérifier les permissions
    user = request.user
    if not user.is_superuser:
        if livraison.type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
        elif livraison.type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            messages.error(request, "Vous n'avez pas accès à cette livraison.")
            return redirect('livraison:liste_livraisons')
    
    if request.method == 'POST':
        livraison.pv_reception_recu = True
        livraison.modifie_par = user
        livraison.save()
        
        messages.success(request, f'PV de réception validé pour la livraison {livraison.numero_commande}.')
        return redirect('livraison:detail_livraison', pk=pk)
    
    context = {
        'livraison': livraison
    }
    return render(request, 'livraison/valider_pv_reception.html', context)


@login_required
def rapports_livraison(request):
    """Rapports et statistiques de livraison"""
    
    # Récupérer les livraisons selon les permissions
    user = request.user
    if user.is_superuser:
        livraisons = Livraison.objects.all()
    elif hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique:
        livraisons = Livraison.objects.filter(type_commande='informatique')
    elif hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau:
        livraisons = Livraison.objects.filter(type_commande='bureau')
    else:
        livraisons = Livraison.objects.none()
    
    # Statistiques générales
    total_livraisons = livraisons.count()
    livraisons_livrees = livraisons.filter(statut_livraison='livree').count()
    livraisons_conformes = livraisons.filter(conforme=True).count()
    pv_recus = livraisons.filter(pv_reception_recu=True).count()
    
    # Par type de commande
    livraisons_informatique = livraisons.filter(type_commande='informatique').count()
    livraisons_bureau = livraisons.filter(type_commande='bureau').count()
    
    # Par statut
    livraisons_par_statut = livraisons.values('statut_livraison').annotate(
        count=Count('id')
    ).order_by('statut_livraison')
    
    # Par fournisseur
    livraisons_par_fournisseur = livraisons.values(
        'commande_informatique__fournisseur__nom'
    ).annotate(
        count=Count('id')
    ).filter(
        commande_informatique__fournisseur__isnull=False
    ).order_by('-count')[:10]
    
    context = {
        'total_livraisons': total_livraisons,
        'livraisons_livrees': livraisons_livrees,
        'livraisons_conformes': livraisons_conformes,
        'pv_recus': pv_recus,
        'livraisons_informatique': livraisons_informatique,
        'livraisons_bureau': livraisons_bureau,
        'livraisons_par_statut': livraisons_par_statut,
        'livraisons_par_fournisseur': livraisons_par_fournisseur,
    }
    
    return render(request, 'livraison/rapports.html', context)


# Vues API pour le formulaire dynamique
@login_required
def api_commandes(request):
    """API pour récupérer les commandes selon le type"""
    user = request.user
    type_commande = request.GET.get('type')
    
    # Vérifier les permissions
    if not user.is_superuser:
        if type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            return JsonResponse({'error': 'Permission refusée'}, status=403)
        elif type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            return JsonResponse({'error': 'Permission refusée'}, status=403)
    
    commandes = []
    
    if type_commande == 'informatique':
        from apps.commande_informatique.models import Commande
        commandes_objs = Commande.objects.select_related('fournisseur').all()
        commandes = [
            {
                'id': cmd.id,
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom,
                'date_commande': cmd.date_commande.strftime('%d/%m/%Y')
            }
            for cmd in commandes_objs
        ]
    elif type_commande == 'bureau':
        from apps.commande_bureau.models import CommandeBureau
        commandes_objs = CommandeBureau.objects.select_related('fournisseur').all()
        commandes = [
            {
                'id': cmd.id,
                'numero_commande': cmd.numero_commande,
                'fournisseur': cmd.fournisseur.nom,
                'date_commande': cmd.date_commande.strftime('%d/%m/%Y')
            }
            for cmd in commandes_objs
        ]
    
    return JsonResponse({'commandes': commandes})


@login_required
def api_commande_details(request, commande_id):
    """API pour récupérer les détails d'une commande"""
    user = request.user
    type_commande = request.GET.get('type')
    
    # Vérifier les permissions
    if not user.is_superuser:
        if type_commande == 'informatique' and not (hasattr(user, 'gestionnaire_informatique') and user.gestionnaire_informatique):
            return JsonResponse({'error': 'Permission refusée'}, status=403)
        elif type_commande == 'bureau' and not (hasattr(user, 'gestionnaire_bureau') and user.gestionnaire_bureau):
            return JsonResponse({'error': 'Permission refusée'}, status=403)
    
    try:
        if type_commande == 'informatique':
            from apps.commande_informatique.models import Commande
            commande = Commande.objects.select_related('fournisseur').prefetch_related('lignes__designation', 'lignes__description').get(id=commande_id)
            
            materiels = []
            montant_total = 0
            nombre_articles = 0
            
            for ligne in commande.lignes.all():
                prix_total_ligne = ligne.quantite * ligne.prix_unitaire
                montant_total += prix_total_ligne
                nombre_articles += ligne.quantite
                
                materiels.append({
                    'id': ligne.id,
                    'designation': ligne.designation.nom,
                    'description': ligne.description.nom if ligne.description else '',
                    'quantite': ligne.quantite,
                    'prix_unitaire': f"{ligne.prix_unitaire:.2f}",
                    'prix_total': f"{prix_total_ligne:.2f}"
                })
            
        elif type_commande == 'bureau':
            from apps.commande_bureau.models import CommandeBureau
            commande = CommandeBureau.objects.select_related('fournisseur').prefetch_related('lignes__designation', 'lignes__description').get(id=commande_id)
            
            materiels = []
            montant_total = 0
            nombre_articles = 0
            
            for ligne in commande.lignes.all():
                prix_total_ligne = ligne.quantite * ligne.prix_unitaire
                montant_total += prix_total_ligne
                nombre_articles += ligne.quantite
                
                materiels.append({
                    'id': ligne.id,
                    'designation': ligne.designation.nom,
                    'description': ligne.description.nom if ligne.description else '',
                    'quantite': ligne.quantite,
                    'prix_unitaire': f"{ligne.prix_unitaire:.2f}",
                    'prix_total': f"{prix_total_ligne:.2f}"
                })
        else:
            return JsonResponse({'error': 'Type de commande invalide'}, status=400)
        
        return JsonResponse({
            'fournisseur': commande.fournisseur.nom,
            'numero_commande': commande.numero_commande,
            'montant_total': f"{montant_total:.2f}",
            'nombre_articles': nombre_articles,
            'materiels': materiels
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Commande introuvable'}, status=404)
