from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Fournisseur
from .forms import FournisseurForm


# Fonctions d'autorisation
def is_superadmin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Super Admin').exists())

def is_gestionnaire_informatique(user):
    return user.is_authenticated and user.groups.filter(name='Gestionnaire Informatique').exists()

def is_gestionnaire_bureau(user):
    return user.is_authenticated and user.groups.filter(name='Gestionnaire Bureau').exists()

def is_superadmin_or_gestionnaire_informatique(user):
    return is_superadmin(user) or is_gestionnaire_informatique(user)

def is_superadmin_or_gestionnaire_bureau(user):
    return is_superadmin(user) or is_gestionnaire_bureau(user)


# Liste fournisseurs filtrée par rôle et catégorie
@user_passes_test(lambda u: is_superadmin_or_gestionnaire_informatique(u) or is_superadmin_or_gestionnaire_bureau(u))
def fournisseur_list(request):
    user = request.user

    if is_superadmin(user):
        fournisseurs = Fournisseur.objects.all()
    elif is_gestionnaire_informatique(user):
        fournisseurs = Fournisseur.objects.filter(categorie='informatique')
    elif is_gestionnaire_bureau(user):
        fournisseurs = Fournisseur.objects.filter(categorie='bureautique')
    else:
        fournisseurs = Fournisseur.objects.none()

    return render(request, 'fournisseur/fournisseur_list.html', {'fournisseurs': fournisseurs})


# Création fournisseur avec contrôle catégorie
@user_passes_test(lambda u: is_superadmin_or_gestionnaire_informatique(u) or is_superadmin_or_gestionnaire_bureau(u))
def fournisseur_create(request):
    user = request.user

    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.save(commit=False)

            # Vérification stricte des catégories selon rôle
            if not is_superadmin(user):
                if is_gestionnaire_informatique(user) and fournisseur.categorie != 'informatique':
                    messages.error(request, "En tant que Gestionnaire Informatique, vous ne pouvez ajouter que des fournisseurs de catégorie informatique.")
                    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})
                if is_gestionnaire_bureau(user) and fournisseur.categorie != 'bureautique':
                    messages.error(request, "En tant que Gestionnaire Bureau, vous ne pouvez ajouter que des fournisseurs de catégorie bureautique.")
                    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})

            # Superadmin peut ajouter toutes catégories
            fournisseur.save()
            messages.success(request, "Fournisseur ajouté avec succès.")
            return redirect('fournisseur:fournisseur_list')
    else:
        form = FournisseurForm()

    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})


# Modification fournisseur avec contrôle catégorie
@user_passes_test(lambda u: is_superadmin_or_gestionnaire_informatique(u) or is_superadmin_or_gestionnaire_bureau(u))
def fournisseur_update(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    user = request.user

    # Contrôle accès catégorie avant modification
    if not is_superadmin(user):
        if is_gestionnaire_informatique(user) and fournisseur.categorie != 'informatique':
            messages.error(request, "Accès refusé à ce fournisseur.")
            return redirect('fournisseur:fournisseur_list')
        if is_gestionnaire_bureau(user) and fournisseur.categorie != 'bureautique':
            messages.error(request, "Accès refusé à ce fournisseur.")
            return redirect('fournisseur:fournisseur_list')

    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            fournisseur_modifie = form.save(commit=False)

            # Validation stricte catégorie au cas où elle est modifiée
            if not is_superadmin(user):
                if is_gestionnaire_informatique(user) and fournisseur_modifie.categorie != 'informatique':
                    messages.error(request, "En tant que Gestionnaire Informatique, vous ne pouvez modifier que des fournisseurs de catégorie informatique.")
                    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})
                if is_gestionnaire_bureau(user) and fournisseur_modifie.categorie != 'bureautique':
                    messages.error(request, "En tant que Gestionnaire Bureau, vous ne pouvez modifier que des fournisseurs de catégorie bureautique.")
                    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})

            fournisseur_modifie.save()
            messages.success(request, "Fournisseur modifié avec succès.")
            return redirect('fournisseur:fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)

    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})


# Suppression fournisseur avec contrôle catégorie
@user_passes_test(lambda u: is_superadmin_or_gestionnaire_informatique(u) or is_superadmin_or_gestionnaire_bureau(u))
def fournisseur_delete(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    user = request.user

    # Contrôle accès avant suppression
    if not is_superadmin(user):
        if is_gestionnaire_informatique(user) and fournisseur.categorie != 'informatique':
            messages.error(request, "Accès refusé à ce fournisseur.")
            return redirect('fournisseur:fournisseur_list')
        if is_gestionnaire_bureau(user) and fournisseur.categorie != 'bureautique':
            messages.error(request, "Accès refusé à ce fournisseur.")
            return redirect('fournisseur:fournisseur_list')

    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé avec succès.")
        return redirect('fournisseur:fournisseur_list')

    return render(request, 'fournisseur/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})