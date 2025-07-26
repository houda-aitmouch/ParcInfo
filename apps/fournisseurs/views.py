from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, GradientFill
from openpyxl.utils import get_column_letter
from .models import Fournisseur
from .forms import FournisseurForm


def is_gestionnaire_ou_superadmin(user):
    return user.groups.filter(name__in=['Gestionnaire Informatique', 'Super Admin']).exists()


@user_passes_test(is_gestionnaire_ou_superadmin)
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()  # récupère tous les fournisseurs
    total = fournisseurs.count()               # compte le nombre total
    return render(request, 'fournisseurs/fournisseur_list.html', {
        'fournisseurs': fournisseurs,
        'total': total,
    })
@user_passes_test(is_gestionnaire_ou_superadmin)
def fournisseur_create(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur ajouté avec succès.")
            return redirect('fournisseurs:fournisseur_list')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseurs/fournisseur_form.html', {
        'form': form,
        'title': 'Ajouter un fournisseur'
    })


@user_passes_test(is_gestionnaire_ou_superadmin)
def fournisseur_update(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur mis à jour avec succès.")
            return redirect('fournisseurs:fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/fournisseur_form.html', {
        'form': form,
        'title': 'Modifier le fournisseur'
    })


@user_passes_test(is_gestionnaire_ou_superadmin)
def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé avec succès.")
        return redirect('fournisseurs:fournisseur_list')
    return render(request, 'fournisseurs/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})


@user_passes_test(is_gestionnaire_ou_superadmin)
def exporter_fournisseurs_excel(request):
    fournisseurs = Fournisseur.objects.all()
    total = fournisseurs.count()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fournisseurs"

    # --- Titre fusionné ---
    titre = "Liste des fournisseurs"
    ws.merge_cells('A1:E1')
    title_cell = ws['A1']
    title_cell.value = titre
    title_cell.font = Font(name='Calibri', size=18, bold=True, color='2C3E50')
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    title_cell.fill = PatternFill("solid", fgColor="D6E4F0")  # Bleu clair doux
    ws.row_dimensions[1].height = 30

    # --- En-têtes ---
    headers = ['Nom', 'IF', 'ICE', 'RC', 'Adresse']
    header_row = 3  # on laisse la ligne 2 vide pour aérer
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_num)
        cell.value = header
        cell.font = Font(name='Segoe UI', size=12, bold=True, color='FFFFFF')
        cell.fill = GradientFill(stop=("4A90E2", "357ABD"))  # dégradé bleu
        cell.alignment = Alignment(horizontal="center", vertical="center")
        thin_border = Border(
            left=Side(style='thin', color='B0C4DE'),
            right=Side(style='thin', color='B0C4DE'),
            top=Side(style='thin', color='B0C4DE'),
            bottom=Side(style='thin', color='B0C4DE'),
        )
        cell.border = thin_border
    ws.row_dimensions[header_row].height = 22

    # --- Corps du tableau ---
    fill_even = PatternFill("solid", fgColor="F7FAFC")  # blanc cassé très clair
    fill_odd = PatternFill("solid", fgColor="FFFFFF")   # blanc pur
    content_font = Font(name='Calibri', size=11, color='2C3E50')  # gris foncé
    thin_border = Border(
        left=Side(style='thin', color='D1D9E6'),
        right=Side(style='thin', color='D1D9E6'),
        top=Side(style='thin', color='D1D9E6'),
        bottom=Side(style='thin', color='D1D9E6'),
    )

    for i, fournisseur in enumerate(fournisseurs, start=header_row + 1):
        fill = fill_even if i % 2 == 0 else fill_odd
        row_values = [
            fournisseur.nom or '',
            fournisseur.if_fiscal or '',
            fournisseur.ice or '',
            fournisseur.registre_commerce or '',
            fournisseur.adresse or '',
        ]
        for col_num, value in enumerate(row_values, 1):
            cell = ws.cell(row=i, column=col_num, value=value)
            cell.font = content_font
            cell.fill = fill
            # Alignement colonne
            if col_num == 1 or col_num == 5:  # Texte à gauche (Nom, Adresse)
                cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            else:  # Numéros centrés
                cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.border = thin_border
        ws.row_dimensions[i].height = 18

    # --- Ligne résumé ---
    summary_row = ws.max_row + 1
    ws.merge_cells(start_row=summary_row, start_column=1, end_row=summary_row, end_column=5)
    summary_cell = ws.cell(row=summary_row, column=1)
    summary_cell.value = f"Nombre total de fournisseurs : {total}"
    summary_cell.font = Font(name='Calibri', size=12, italic=True, color='4A4A4A')
    summary_cell.alignment = Alignment(horizontal='right', vertical='center')
    summary_cell.fill = PatternFill("solid", fgColor="E2E8F0")  # Gris clair
    ws.row_dimensions[summary_row].height = 20

    # --- Ajustement largeur colonnes ---
    for col_num, _ in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        max_length = max(
            (len(str(ws.cell(row=row, column=col_num).value or "")) for row in range(1, ws.max_row + 1)),
            default=10
        )
        adjusted_width = min(max(max_length + 5, 15), 60)  # min 15, max 60 pour confort lecture
        ws.column_dimensions[col_letter].width = adjusted_width

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=liste_fournisseurs.xlsx'
    wb.save(response)
    return response