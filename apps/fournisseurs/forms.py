from django import forms
from .models import Fournisseur

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'if_fiscal', 'ice', 'registre_commerce', 'adresse']
        labels = {
            'nom': 'Nom du Fournisseur',
            'if_fiscal': 'Identifiant Fiscal (IF)',
            'ice': 'Identifiant Commun de l’Entreprise (ICE)',
            'registre_commerce': 'Registre du Commerce (RC)',
            'adresse': 'Adresse',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'if_fiscal': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'ice': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'registre_commerce': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'adresse': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 3}),
        }