# apps/commande/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Commande, LigneCommande, Designation, Description
from apps.fournisseurs.models import Fournisseur

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [
            'mode_passation', 'numero_commande', 'fournisseur',
            'date_commande', 'date_reception', 'numero_facture',
            'duree_garantie_valeur', 'duree_garantie_unite',
        ]
        widgets = {
            'date_commande': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded px-3 py-2'}),
            'date_reception': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded px-3 py-2'}),
            'numero_facture': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'duree_garantie_valeur': forms.NumberInput(attrs={'min': 1, 'class': 'w-full border rounded px-3 py-2'}),
            'duree_garantie_unite': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les queryset si nécessaire
        self.fields['fournisseur'].queryset = Fournisseur.objects.all().order_by('nom')

class LigneCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['designation', 'description', 'quantite', 'prix_unitaire']
        widgets = {
            'designation': forms.Select(),
            'description': forms.Select(),
            'quantite': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'min': '1'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('nom')
        # Les descriptions seront chargées dynamiquement via AJAX
        self.fields['description'].queryset = Description.objects.none()

# Formset pour gérer plusieurs lignes de commande
LigneCommandeFormSet = inlineformset_factory(
    Commande,
    LigneCommande,
    form=LigneCommandeForm,
    extra=0,  # Pas de formulaire vide par défaut
    can_delete=True,
    min_num=1,  # Au moins une ligne de commande
    validate_min=True,
)