# apps/fournisseur/forms.py

from django import forms
from .models import Fournisseur

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'  # ou liste précise des champs comme ['nom', 'email', 'categorie', ...]