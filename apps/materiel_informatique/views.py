from django.shortcuts import render, redirect, get_object_or_404
from .models import MaterielInformatique
from .forms import MaterielInformatiqueForm
from django.http import JsonResponse
from apps.commande_informatique.models import LigneCommande
from django.core.exceptions import PermissionDenied
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

def is_gestionnaire_ou_superadmin(user):
    return user.groups.filter(name__in=['Gestionnaire Informatique', 'Super Admin']).exists()


def liste_materiels(request):
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    materiels = MaterielInformatique.objects.all()
    return render(request, 'materiel_informatique/liste_materiels.html', {'materiels': materiels})

def ajouter_materiel(request):
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = MaterielInformatiqueForm(request.POST)
        if form.is_valid():
            materiel = form.save()
            return redirect('materiel_informatique:liste_materiels')
    else:
        form = MaterielInformatiqueForm()
    return render(request, 'materiel_informatique/ajouter_materiel.html', {'form': form})

def modifier_materiel(request, pk):
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    materiel = get_object_or_404(MaterielInformatique, pk=pk)
    if request.method == 'POST':
        form = MaterielInformatiqueForm(request.POST, instance=materiel)
        if form.is_valid():
            materiel = form.save()
            return redirect('materiel_informatique:liste_materiels')
    else:
        form = MaterielInformatiqueForm(instance=materiel)
    return render(request, 'materiel_informatique/modifier_materiel.html', {
        'form': form,
        'is_edit': True,
        'materiel': materiel,
    })

def supprimer_materiel(request, pk):
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    materiel = get_object_or_404(MaterielInformatique, pk=pk)
    if request.method == 'POST':
        materiel.delete()
        return redirect('materiel_informatique:liste_materiels')
    return render(request, 'materiel_informatique/confirmer_suppression.html', {'materiel': materiel})

def lignes_commande_par_commande(request, commande_id):
    lignes = LigneCommande.objects.filter(commande_id=commande_id).select_related('designation', 'description', 'commande__fournisseur', 'commande')
    data = [
        {
            'id': ligne.id,
            'designation': ligne.designation.nom,
            'designation_id': ligne.designation.id,
            'description': ligne.description.nom,
            'description_id': ligne.description.id,
            'prix_unitaire': str(ligne.prix_unitaire),
            'fournisseur': ligne.commande.fournisseur.nom if ligne.commande.fournisseur else '',
            'numero_facture': ligne.commande.numero_facture or '',
            'date_reception': ligne.commande.date_reception.strftime('%Y-%m-%d') if ligne.commande.date_reception else '',
            'duree_garantie_valeur': getattr(ligne.commande, 'duree_garantie_valeur', ''),
            'duree_garantie_unite': getattr(ligne.commande, 'duree_garantie_unite', ''),
        }
        for ligne in lignes
    ]
    return JsonResponse(data, safe=False)

def export_materiels_excel(request):
    if not is_gestionnaire_ou_superadmin(request.user):
        raise PermissionDenied
    materiels = MaterielInformatique.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Matériels"

    # En-tête
    headers = [
        "Commande", "Numéro de série", "Code inventaire", "Désignation", "Description", "Prix unitaire",
        "Fournisseur", "N° Facture", "Date service", "Date fin garantie", "Statut", "Utilisateur",
        "Lieu stockage", "Public", "Observation"
    ]
    ws.append(headers)

    # Styles
    header_fill = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    for col_num, column_title in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    # Lignes
    for idx, mat in enumerate(materiels, start=2):
        ws.append([
            getattr(mat.ligne_commande.commande, 'numero_commande', ''),
            mat.numero_serie,
            mat.code_inventaire,
            getattr(mat.ligne_commande.designation, 'nom', ''),
            getattr(mat.ligne_commande.description, 'nom', ''),
            mat.ligne_commande.prix_unitaire,
            getattr(mat.ligne_commande.commande.fournisseur, 'nom', ''),
            getattr(mat.ligne_commande.commande, 'numero_facture', ''),
            mat.date_service_calculee.strftime('%d/%m/%Y') if mat.date_service_calculee else '',
            mat.date_fin_garantie_calculee.strftime('%d/%m/%Y') if mat.date_fin_garantie_calculee else '',
            dict(mat._meta.get_field('statut').choices).get(mat.statut, mat.statut),
            str(mat.utilisateur) if mat.utilisateur else '',
            dict(mat._meta.get_field('lieu_stockage').choices).get(mat.lieu_stockage, mat.lieu_stockage),
            "Oui" if mat.public else "Non",
            mat.observation,
        ])
        # Alternance de couleur de ligne
        fill = PatternFill(start_color="E0E7FF" if idx % 2 == 0 else "FFFFFF", end_color="E0E7FF" if idx % 2 == 0 else "FFFFFF", fill_type="solid")
        for col in range(1, len(headers)+1):
            cell = ws.cell(row=idx, column=col)
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center")
            if idx % 2 == 0:
                cell.fill = fill

    # Ajuste la largeur des colonnes
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column].width = max_length + 3

    # Réponse HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=liste_materiels.xlsx'
    wb.save(response)
    return response

@login_required
def mes_equipements_informatiques(request):
    equipements = MaterielInformatique.objects.filter(utilisateur=request.user, statut='affecte')
    return render(request, 'materiel_informatique/mes_equipements_informatiques.html', {'equipements': equipements})
