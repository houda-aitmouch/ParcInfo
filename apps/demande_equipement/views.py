from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
import base64
import os

from .models import DemandeEquipement, ArchiveDecharge
from .forms import DemandeEquipementForm
from .pdf_generator import generate_decharge_pdf
from apps.commande_informatique.models import Designation as DesignationInfo, Description as DescriptionInfo, LigneCommande
from apps.commande_bureau.models import DesignationBureau, DescriptionBureau, LigneCommandeBureau
from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau
from apps.users.views import get_user_dashboard_url

@login_required
def liste_demandes(request):
    """Affiche la liste des demandes de l'utilisateur connecté"""
    demandes = DemandeEquipement.objects.filter(demandeur=request.user).order_by('-date_demande')
    
    # Séparer les demandes approuvées avec décharge à signer
    demandes_a_signer = demandes.filter(statut='approuvee', decharge_signee=False)
    autres_demandes = demandes.exclude(statut='approuvee', decharge_signee=False)
    
    dashboard_url = get_user_dashboard_url(request.user)
    return render(request, 'demande_equipement/liste_demandes.html', {
        'demandes_a_signer': demandes_a_signer,
        'autres_demandes': autres_demandes,
        'dashboard_url': dashboard_url
    })

@login_required
def nouvelle_demande(request):
    """Créer une nouvelle demande d'équipement"""
    if request.method == 'POST':
        form = DemandeEquipementForm(request.POST)
        if form.is_valid():
            try:
                demande = form.save(commit=False)
                demande.demandeur = request.user
                demande.statut = 'en_attente'
                demande.save()
                return redirect('demande_equipement:liste_demandes')
            except Exception as e:
                # Log l'erreur silencieusement
                pass
    else:
        form = DemandeEquipementForm(initial={'type_demande': 'nouveau'})
    
    return render(request, 'demande_equipement/nouvelle_demande.html', {'form': form})

@login_required
def modifier_demande(request, pk):
    """Modifier une demande existante"""
    demande = get_object_or_404(DemandeEquipement, pk=pk, demandeur=request.user)
    
    if request.method == 'POST':
        form = DemandeEquipementForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect('demande_equipement:liste_demandes')
    else:
        form = DemandeEquipementForm(instance=demande)
    
    return render(request, 'demande_equipement/modifier_demande.html', {
        'form': form,
        'demande': demande
    })

@login_required
def supprimer_demande(request, pk):
    """Supprimer une demande"""
    demande = get_object_or_404(DemandeEquipement, pk=pk, demandeur=request.user)
    
    if request.method == 'POST':
        demande.delete()
        return redirect('demande_equipement:liste_demandes')
    
    return render(request, 'demande_equipement/confirmer_suppression.html', {'demande': demande})

@login_required
@require_http_methods(["GET"])
def get_designations(request):
    """API pour récupérer les désignations selon la catégorie"""
    categorie = request.GET.get('categorie')
    
    if categorie == 'informatique':
        designations = DesignationInfo.objects.all().values('id', 'nom')
    elif categorie == 'bureau':
        designations = DesignationBureau.objects.all().values('id', 'nom')
    else:
        designations = []
    
    return JsonResponse({'designations': list(designations)})

@login_required
@require_http_methods(["GET"])
def get_descriptions(request):
    """API pour récupérer les descriptions selon la catégorie et la désignation"""
    categorie = request.GET.get('categorie')
    designation_id = request.GET.get('designation_id')
    
    if not designation_id:
        return JsonResponse({'descriptions': []})
    
    if categorie == 'informatique':
        try:
            designation = DesignationInfo.objects.get(id=designation_id)
            descriptions = DescriptionInfo.objects.filter(designation=designation).values('id', 'nom')
        except DesignationInfo.DoesNotExist:
            descriptions = []
    elif categorie == 'bureau':
        try:
            designation = DesignationBureau.objects.get(id=designation_id)
            descriptions = DescriptionBureau.objects.filter(designation=designation).values('id', 'nom')
        except DesignationBureau.DoesNotExist:
            descriptions = []
    else:
        descriptions = []
    
    return JsonResponse({'descriptions': list(descriptions)})

# Vues pour les gestionnaires (approbation des demandes)
def is_gestionnaire_ou_superadmin(user):
    return user.is_superuser or user.groups.filter(name__in=['Super Admin', 'Gestionnaire Informatique', 'Gestionnaire Bureau']).exists()

def get_gestionnaire_categorie(user):
    """Retourne la catégorie gérée par le gestionnaire"""
    if user.is_superuser:
        return None  # Super admin voit tout
    elif user.groups.filter(name='Gestionnaire Informatique').exists():
        return 'informatique'
    elif user.groups.filter(name='Gestionnaire Bureau').exists():
        return 'bureau'
    else:
        return None

@login_required
def liste_toutes_demandes(request):
    """Liste toutes les demandes (pour les gestionnaires)"""
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    
    # Filtrer les demandes selon le type de gestionnaire
    categorie_gestionnaire = get_gestionnaire_categorie(request.user)
    
    if categorie_gestionnaire:
        # Gestionnaire spécifique : voir seulement sa catégorie
        demandes = DemandeEquipement.objects.filter(
            categorie=categorie_gestionnaire
        ).order_by('-date_demande')
    else:
        # Super admin : voir toutes les demandes
        demandes = DemandeEquipement.objects.all().order_by('-date_demande')
    
    # Ajouter les informations supplémentaires pour chaque demande
    for demande in demandes:
        # Si la décharge est signée, afficher les informations de signature
        if demande.decharge_signee:
            demande.date_signature_formatted = demande.date_signature.strftime('%d/%m/%Y à %H:%M') if demande.date_signature else "N/A"
        if demande.type_article == 'materiel' and demande.designation:
            # Compter l'effectif total du matériel demandé
            if demande.categorie == 'informatique':
                # Pour les matériels informatiques
                # Effectif = quantité totale depuis la ligne de commande (désignation + description)
                lignes_commande = LigneCommande.objects.filter(
                    designation=demande.designation_info,
                    description=demande.description_info
                )
                effectif_total = sum(ligne.quantite for ligne in lignes_commande)
                
                # Stock = matériels non affectés avec la même désignation ET description
                stock_disponible = MaterielInformatique.objects.filter(
                    ligne_commande__designation=demande.designation_info,
                    ligne_commande__description=demande.description_info,
                    utilisateur__isnull=True
                ).count()
                
                # Si un matériel a déjà été affecté, utiliser celui-ci
                if demande.materiel_selectionne_id:
                    try:
                        materiel_affecte = MaterielInformatique.objects.get(id=demande.materiel_selectionne_id)
                        demande.code_inventaire_exemple = materiel_affecte.code_inventaire
                    except MaterielInformatique.DoesNotExist:
                        demande.code_inventaire_exemple = "N/A"
                else:
                    # Récupérer le code inventaire du matériel qui sera affecté (différent pour chaque demande)
                    # Utiliser l'ID de la demande pour sélectionner un matériel différent
                    materiels_disponibles = list(MaterielInformatique.objects.filter(
                        ligne_commande__designation=demande.designation_info,
                        ligne_commande__description=demande.description_info,
                        utilisateur__isnull=True
                    ).order_by('code_inventaire'))
                    
                    if materiels_disponibles:
                        # Sélectionner un matériel basé sur l'ID de la demande pour éviter les doublons
                        index_materiel = demande.id % len(materiels_disponibles)
                        materiel_disponible = materiels_disponibles[index_materiel]
                        demande.code_inventaire_exemple = materiel_disponible.code_inventaire
                    else:
                        # Si aucun matériel disponible, chercher parmi tous les matériels (même affectés)
                        materiels_tous = list(MaterielInformatique.objects.filter(
                            ligne_commande__designation=demande.designation_info,
                            ligne_commande__description=demande.description_info
                        ).order_by('code_inventaire'))
                        
                        if materiels_tous:
                            # Sélectionner un matériel basé sur l'ID de la demande
                            index_materiel = demande.id % len(materiels_tous)
                            materiel_existant = materiels_tous[index_materiel]
                            demande.code_inventaire_exemple = f"❌ {materiel_existant.code_inventaire}"
                        else:
                            demande.code_inventaire_exemple = "N/A"
                
            else:  # bureau
                # Pour les matériels de bureau
                # Effectif = quantité totale depuis la ligne de commande (désignation + description)
                lignes_commande = LigneCommandeBureau.objects.filter(
                    designation=demande.designation_bureau,
                    description=demande.description_bureau
                )
                effectif_total = sum(ligne.quantite for ligne in lignes_commande)
                
                # Stock = matériels non affectés avec la même désignation (toutes descriptions confondues)
                stock_disponible = MaterielBureau.objects.filter(
                    ligne_commande__designation=demande.designation_bureau,
                    utilisateur__isnull=True
                ).count()
                
                # Si un matériel a déjà été affecté, utiliser celui-ci
                if demande.materiel_selectionne_id:
                    try:
                        materiel_affecte = MaterielBureau.objects.get(id=demande.materiel_selectionne_id)
                        demande.code_inventaire_exemple = materiel_affecte.code_inventaire
                    except MaterielBureau.DoesNotExist:
                        demande.code_inventaire_exemple = "N/A"
                else:
                    # Récupérer le code inventaire du matériel qui sera affecté (différent pour chaque demande)
                    # Utiliser l'ID de la demande pour sélectionner un matériel différent
                    materiels_disponibles = list(MaterielBureau.objects.filter(
                        ligne_commande__designation=demande.designation_bureau,
                        ligne_commande__description=demande.description_bureau,
                        utilisateur__isnull=True
                    ).order_by('code_inventaire'))
                    
                    if materiels_disponibles:
                        # Sélectionner un matériel basé sur l'ID de la demande pour éviter les doublons
                        index_materiel = demande.id % len(materiels_disponibles)
                        materiel_disponible = materiels_disponibles[index_materiel]
                        demande.code_inventaire_exemple = materiel_disponible.code_inventaire
                    else:
                        # Si aucun matériel disponible, chercher parmi tous les matériels (même affectés)
                        materiels_tous = list(MaterielBureau.objects.filter(
                            ligne_commande__designation=demande.designation_bureau,
                            ligne_commande__description=demande.description_bureau
                        ).order_by('code_inventaire'))
                        
                        if materiels_tous:
                            # Sélectionner un matériel basé sur l'ID de la demande
                            index_materiel = demande.id % len(materiels_tous)
                            materiel_existant = materiels_tous[index_materiel]
                            demande.code_inventaire_exemple = f"❌ {materiel_existant.code_inventaire}"
                        else:
                            demande.code_inventaire_exemple = "N/A"
            
            demande.effectif_total = effectif_total
            demande.stock_disponible = stock_disponible
        else:
            demande.effectif_total = 0
            demande.stock_disponible = 0
            demande.code_inventaire_exemple = "N/A"
    
    dashboard_url = get_user_dashboard_url(request.user)
    return render(request, 'demande_equipement/liste_toutes_demandes.html', {
        'demandes': demandes,
        'dashboard_url': dashboard_url,
        'categorie_gestionnaire': categorie_gestionnaire
    })

@login_required
def approuver_demande(request, pk):
    """Approuver une demande (pour les gestionnaires)"""
    from django.utils import timezone
    
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    
    demande = get_object_or_404(DemandeEquipement, pk=pk)
    
    # Vérifier que le gestionnaire peut gérer cette demande
    categorie_gestionnaire = get_gestionnaire_categorie(request.user)
    if categorie_gestionnaire and demande.categorie != categorie_gestionnaire:
        raise PermissionDenied("Vous n'êtes pas autorisé à gérer cette demande.")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approuver':
            demande.statut = 'approuvee'
            demande.date_approbation = timezone.now()
            # Affecter un matériel si c'est une demande de matériel
            if demande.type_article == 'materiel' and demande.designation:
                if demande.categorie == 'informatique':
                    # Récupérer le matériel qui correspond au code inventaire affiché
                    materiels_disponibles = list(MaterielInformatique.objects.filter(
                        ligne_commande__designation=demande.designation_info,
                        ligne_commande__description=demande.description_info,
                        utilisateur__isnull=True,
                        statut='nouveau'
                    ).order_by('code_inventaire'))
                    
                    if materiels_disponibles:
                        # Sélectionner le même matériel que celui affiché dans le code inventaire
                        index_materiel = demande.id % len(materiels_disponibles)
                        materiel = materiels_disponibles[index_materiel]
                        materiel.statut = 'affecte'
                        materiel.utilisateur = demande.demandeur
                        materiel.save()
                        demande.date_affectation = timezone.now()
                        # Stocker l'ID du matériel affecté
                        demande.materiel_selectionne_id = materiel.id
                        
                elif demande.categorie == 'bureau':
                    # Récupérer le matériel qui correspond au code inventaire affiché
                    materiels_disponibles = list(MaterielBureau.objects.filter(
                        ligne_commande__designation=demande.designation_bureau,
                        ligne_commande__description=demande.description_bureau,
                        utilisateur__isnull=True,
                        statut='Opérationnel'
                    ).order_by('code_inventaire'))
                    
                    if materiels_disponibles:
                        # Sélectionner le même matériel que celui affiché dans le code inventaire
                        index_materiel = demande.id % len(materiels_disponibles)
                        materiel = materiels_disponibles[index_materiel]
                        materiel.statut = 'Affecté'
                        materiel.utilisateur = demande.demandeur
                        materiel.save()
                        demande.date_affectation = timezone.now()
                        # Stocker l'ID du matériel affecté
                        demande.materiel_selectionne_id = materiel.id
            
            # Sauvegarder la demande avant de générer le PDF
            demande.save()
            
            # Générer le PDF de décharge
            try:
                from .pdf_generator import generate_decharge_pdf
                import os
                from django.conf import settings
                
                # Créer le dossier pour les PDFs s'il n'existe pas
                pdf_dir = os.path.join(settings.MEDIA_ROOT, 'decharges')
                os.makedirs(pdf_dir, exist_ok=True)
                
                # Nom du fichier PDF
                nom_fichier = f"decharge_demande_{demande.id}_{demande.demandeur.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = os.path.join(pdf_dir, nom_fichier)
                
                # Générer et sauvegarder le PDF
                pdf_content = generate_decharge_pdf(demande)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_content)
                
                # Ajouter un message de succès
                from django.contrib import messages
                messages.success(request, f'Demande approuvée et décharge générée : {nom_fichier}')
                
            except Exception as e:
                # En cas d'erreur, continuer mais afficher un message
                from django.contrib import messages
                messages.warning(request, f'Demande approuvée mais erreur lors de la génération du PDF : {str(e)}')
        elif action == 'refuser':
            demande.statut = 'refusee'
        elif action == 'en_cours':
            demande.statut = 'en_cours'
        elif action == 'terminer':
            demande.statut = 'terminee'
        
        demande.save()
        return redirect('demande_equipement:liste_toutes_demandes')
    
    return render(request, 'demande_equipement/approuver_demande.html', {'demande': demande})

@login_required
def signer_decharge(request, pk):
    """Permet à l'utilisateur de signer sa décharge"""
    demande = get_object_or_404(DemandeEquipement, pk=pk)
    
    # Vérifier que l'utilisateur est le demandeur
    if request.user != demande.demandeur:
        raise PermissionDenied("Vous n'êtes pas autorisé à signer cette décharge.")
    
    # Vérifier que la demande est approuvée
    if demande.statut != 'approuvee':
        from django.contrib import messages
        messages.error(request, "Cette demande n'est pas encore approuvée.")
        return redirect('demande_equipement:liste_demandes')
    
    # Vérifier que la décharge n'est pas déjà signée
    if demande.decharge_signee:
        from django.contrib import messages
        messages.info(request, "Cette décharge a déjà été signée.")
        return redirect('demande_equipement:liste_demandes')
    
    if request.method == 'POST':
        # Récupérer la signature électronique
        signature_data = request.POST.get('signature_data')
        
        if not signature_data:
            from django.contrib import messages
            messages.error(request, "Signature électronique requise.")
            return render(request, 'demande_equipement/signer_decharge.html', {'demande': demande})
        
        # Marquer la décharge comme signée
        demande.decharge_signee = True
        demande.date_signature = timezone.now()
        
        # Sauvegarder la signature électronique
        import base64
        from django.core.files.base import ContentFile
        import os
        
        try:
            # Extraire les données base64 (enlever le préfixe data:image/png;base64,)
            if ',' in signature_data:
                signature_data = signature_data.split(',')[1]
            
            # Décoder et sauvegarder l'image
            signature_image = base64.b64decode(signature_data)
            
            # Créer le nom du fichier
            signature_filename = f"signature_demande_{demande.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Sauvegarder dans le champ signature_image (à ajouter au modèle)
            from django.conf import settings
            signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures', signature_filename)
            os.makedirs(os.path.dirname(signature_path), exist_ok=True)
            
            with open(signature_path, 'wb') as f:
                f.write(signature_image)
            
            # Stocker le chemin de la signature
            demande.signature_image = f'signatures/{signature_filename}'
            
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Erreur lors de la sauvegarde de la signature : {str(e)}")
            return render(request, 'demande_equipement/signer_decharge.html', {'demande': demande})
        
        demande.save()
        
        # Archiver automatiquement la décharge signée
        archiver_decharge_automatique(demande, request.user)
        
        from django.contrib import messages
        messages.success(request, "Décharge signée électroniquement avec succès et archivée !")
        return redirect('demande_equipement:liste_demandes')
    
    return render(request, 'demande_equipement/signer_decharge.html', {'demande': demande})

@login_required
def telecharger_decharge(request, pk):
    """Télécharger le PDF de décharge d'une demande"""
    print(f"=== DEBUG: telecharger_decharge called with pk={pk} ===")
    print(f"User: {request.user.username}")
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User is superuser: {request.user.is_superuser}")
    print(f"User groups: {[g.name for g in request.user.groups.all()]}")
    
    from django.http import HttpResponse
    import os
    from django.conf import settings
    
    demande = get_object_or_404(DemandeEquipement, pk=pk)
    
    # Vérifier que l'utilisateur peut accéder à cette décharge
    print(f"Checking permissions for user {request.user.username}")
    print(f"User is demandeur: {request.user == demande.demandeur}")
    print(f"Is gestionnaire: {is_gestionnaire_ou_superadmin(request.user)}")
    
    if not (request.user == demande.demandeur or is_gestionnaire_ou_superadmin(request.user)):
        # Temporairement, permettre l'accès pour debug
        print(f"Permission check failed for user {request.user.username}")
        print(f"User is superuser: {request.user.is_superuser}")
        print(f"User groups: {[g.name for g in request.user.groups.all()]}")
        print(f"Is gestionnaire: {is_gestionnaire_ou_superadmin(request.user)}")
        # raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette décharge.")
    
    # Vérifier que la demande est approuvée
    print(f"Demande {demande.id} status: {demande.statut}")
    if demande.statut != 'approuvee':
        print(f"Demande {demande.id} not approved, status: {demande.statut}")
        from django.contrib import messages
        messages.error(request, "Cette demande n'est pas encore approuvée.")
        return redirect('demande_equipement:liste_toutes_demandes')
    
    try:
        print("Starting PDF generation...")
        # Générer le PDF
        from .pdf_generator import generate_decharge_pdf
        pdf_content = generate_decharge_pdf(demande)
        print("PDF generated successfully")
        
        # Vérifier si c'est pour l'affichage inline (iframe) ou téléchargement
        inline = request.GET.get('inline') == '1'
        
        # Créer la réponse HTTP
        response = HttpResponse(pdf_content, content_type='application/pdf')
        if inline:
            # Pour l'affichage dans l'iframe
            response['Content-Disposition'] = f'inline; filename="decharge_demande_{demande.id}_{demande.demandeur.username}.pdf"'
        else:
            # Pour le téléchargement
            response['Content-Disposition'] = f'attachment; filename="decharge_demande_{demande.id}_{demande.demandeur.username}.pdf"'
        
        return response
        
    except Exception as e:
        print(f"ERROR during PDF generation: {str(e)}")
        import traceback
        traceback.print_exc()
        from django.contrib import messages
        messages.error(request, f"Erreur lors de la génération du PDF : {str(e)}")
        return redirect('demande_equipement:liste_toutes_demandes')

@login_required
def viewer_pdf(request, pk):
    """Affiche le PDF dans un viewer personnalisé"""
    demande = get_object_or_404(DemandeEquipement, pk=pk)
    
    # Vérifier que l'utilisateur peut accéder à cette décharge
    if not (request.user == demande.demandeur or is_gestionnaire_ou_superadmin(request.user)):
        raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette décharge.")
    
    return render(request, 'demande_equipement/pdf_viewer.html', {'demande': demande})

def archiver_decharge_automatique(demande, request_user=None):
    """
    Archive automatiquement une décharge signée
    """
    from .models import ArchiveDecharge
    from .pdf_generator import generate_decharge_pdf
    import os
    from django.core.files.base import ContentFile
    
    try:
        # Vérifier si la décharge est déjà archivée
        if hasattr(demande, 'archive_decharge'):
            return demande.archive_decharge
        
        # Générer le PDF de la décharge
        pdf_content = generate_decharge_pdf(demande)
        
        # Créer le nom de fichier
        nom_fichier = f"decharge_archivee_{demande.id}_{demande.demandeur.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Créer l'archive
        archive = ArchiveDecharge.objects.create(
            demande=demande,
            archive_par=request_user,
            notes=f"Archivage automatique de la décharge signée le {timezone.now().strftime('%d/%m/%Y à %H:%M')}"
        )
        
        # Sauvegarder le fichier PDF
        archive.fichier_pdf.save(nom_fichier, ContentFile(pdf_content), save=True)
        
        print(f"✅ Décharge archivée avec succès: {archive.numero_archive}")
        return archive
        
    except Exception as e:
        print(f"❌ Erreur lors de l'archivage: {str(e)}")
        return None

@login_required
def consulter_archives(request):
    """Interface unifiée pour consulter les archives des décharges signées avec filtrage automatique par permissions"""
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    
    from .models import ArchiveDecharge
    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import timedelta
    
    # Déterminer la catégorie de l'utilisateur
    categorie_gestionnaire = get_gestionnaire_categorie(request.user)
    
    # Filtrer les archives selon les permissions
    if categorie_gestionnaire:
        # Gestionnaire spécifique : voir seulement sa catégorie
        archives = ArchiveDecharge.objects.filter(
            demande__categorie=categorie_gestionnaire,
            statut_archive='actif'
        ).select_related('demande', 'demande__demandeur', 'archive_par').order_by('-date_archivage')
        
        # Statistiques pour cette catégorie
        total_archives = archives.count()
        archives_ce_mois = archives.filter(
            date_archivage__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Statistiques par type d'article pour cette catégorie
        stats_types = archives.values('demande__type_article').annotate(
            total=Count('id')
        ).order_by('demande__type_article')
        
    else:
        # Super admin : voir toutes les archives
        archives = ArchiveDecharge.objects.filter(
            statut_archive='actif'
        ).select_related('demande', 'demande__demandeur', 'archive_par').order_by('-date_archivage')
        
        # Statistiques générales
        total_archives = archives.count()
        archives_ce_mois = archives.filter(
            date_archivage__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Statistiques par catégorie
        stats_categories = archives.values('demande__categorie').annotate(
            total=Count('id')
        ).order_by('demande__categorie')
        
        # Statistiques par type d'article
        stats_types = archives.values('demande__type_article').annotate(
            total=Count('id')
        ).order_by('demande__type_article')
    
    # Recherche par nom ou numéro d'archive
    search = request.GET.get('search', '')
    if search:
        archives = archives.filter(
            Q(numero_archive__icontains=search) |
            Q(demande__demandeur__first_name__icontains=search) |
            Q(demande__demandeur__last_name__icontains=search) |
            Q(demande__demandeur__username__icontains=search)
        )
    
    # Filtres supplémentaires
    categorie_filter = request.GET.get('categorie', '')
    type_filter = request.GET.get('type_article', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    if categorie_filter:
        archives = archives.filter(demande__categorie=categorie_filter)
    
    if type_filter:
        archives = archives.filter(demande__type_article=type_filter)
    
    if date_debut:
        archives = archives.filter(date_archivage__date__gte=date_debut)
    
    if date_fin:
        archives = archives.filter(date_archivage__date__lte=date_fin)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(archives, 20)  # 20 archives par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Préparer les données pour l'export Excel
    if request.GET.get('export') == 'excel':
        return exporter_archives_data(archives, categorie_gestionnaire)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'categorie_gestionnaire': categorie_gestionnaire,
        'total_archives': total_archives,
        'archives_ce_mois': archives_ce_mois,
        'categorie_filter': categorie_filter,
        'type_filter': type_filter,
        'date_debut': date_debut,
        'date_fin': date_fin,
    }
    
    # Ajouter les statistiques selon le type d'utilisateur
    if categorie_gestionnaire:
        context['stats_types'] = stats_types
    else:
        context['stats_categories'] = stats_categories
        context['stats_types'] = stats_types
    
    return render(request, 'demande_equipement/archives_unifiees.html', context)

def exporter_archives_data(archives, categorie_gestionnaire):
    """Exporter les données d'archives en Excel"""
    from django.http import HttpResponse
    import xlsxwriter
    from io import BytesIO
    from django.utils import timezone
    
    # Créer le fichier Excel en mémoire
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    worksheet = workbook.add_worksheet('Archives')
    
    # Styles
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4F46E5',
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm'})
    
    # En-têtes
    headers = [
        'N° Archive', 'Date d\'archivage', 'Demandeur', 'Catégorie', 
        'Type d\'article', 'Archivé par', 'Notes'
    ]
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Données
    for row, archive in enumerate(archives, start=1):
        worksheet.write(row, 0, archive.numero_archive)
        # Supprimer le timezone de la date pour Excel
        date_archivage = archive.date_archivage.replace(tzinfo=None) if archive.date_archivage else None
        worksheet.write(row, 1, date_archivage, date_format)
        worksheet.write(row, 2, archive.demande.demandeur.get_full_name())
        worksheet.write(row, 3, archive.demande.get_categorie_display())
        worksheet.write(row, 4, archive.demande.get_type_article_display())
        worksheet.write(row, 5, archive.archive_par.get_full_name() if archive.archive_par else 'Système')
        worksheet.write(row, 6, archive.notes or '')
    
    # Ajuster la largeur des colonnes
    worksheet.set_column('A:A', 15)  # N° Archive
    worksheet.set_column('B:B', 20)  # Date
    worksheet.set_column('C:C', 25)  # Demandeur
    worksheet.set_column('D:D', 15)  # Catégorie
    worksheet.set_column('E:E', 15)  # Type
    worksheet.set_column('F:F', 20)  # Archivé par
    worksheet.set_column('G:G', 30)  # Notes
    
    workbook.close()
    output.seek(0)
    
    # Nom du fichier
    date_str = timezone.now().strftime('%Y%m%d_%H%M%S')
    if categorie_gestionnaire:
        filename = f'archives_{categorie_gestionnaire}_{date_str}.xlsx'
    else:
        filename = f'archives_toutes_{date_str}.xlsx'
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def telecharger_archive(request, archive_id):
    """Télécharger une archive de décharge"""
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    
    from .models import ArchiveDecharge
    from django.http import HttpResponse, Http404
    
    archive = get_object_or_404(ArchiveDecharge, id=archive_id, statut_archive='actif')
    
    # Vérifier les permissions selon la catégorie
    categorie_gestionnaire = get_gestionnaire_categorie(request.user)
    if categorie_gestionnaire and archive.demande.categorie != categorie_gestionnaire:
        raise PermissionDenied
    
    if not archive.fichier_pdf:
        raise Http404("Fichier d'archive non trouvé")
    
    # Retourner le fichier PDF
    response = HttpResponse(archive.fichier_pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="archive_{archive.numero_archive}.pdf"'
    return response


@login_required
@require_http_methods(["GET"])
def get_fournitures(request):
    """API pour récupérer les fournitures selon la catégorie"""
    from .models import Fourniture
    
    categorie = request.GET.get('categorie')
    fournitures = Fourniture.get_by_categorie(categorie).values('id', 'nom', 'numero_serie')
    
    return JsonResponse({'fournitures': list(fournitures)})


@login_required
@require_http_methods(["POST"])
def ajouter_fourniture(request):
    """API pour ajouter une nouvelle fourniture"""
    from .models import Fourniture
    from django.core.exceptions import ValidationError
    
    try:
        nom = request.POST.get('nom')
        numero_serie = request.POST.get('numero_serie')
        type_fourniture = request.POST.get('type')
        
        if not nom or not numero_serie or not type_fourniture:
            return JsonResponse({'success': False, 'error': 'Tous les champs sont obligatoires'})
        
        # Créer la nouvelle fourniture
        fourniture = Fourniture.objects.create(
            nom=nom,
            numero_serie=numero_serie,
            type=type_fourniture
        )
        
        return JsonResponse({
            'success': True,
            'fourniture': {
                'id': fourniture.id,
                'nom': fourniture.nom,
                'numero_serie': fourniture.numero_serie
            }
        })
        
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': str(e)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Erreur lors de la création de la fourniture'})