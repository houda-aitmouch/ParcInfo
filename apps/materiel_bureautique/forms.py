from django import forms
from .models import MaterielBureau
from apps.commande_bureau.models import CommandeBureau, LigneCommandeBureau
from django.contrib.auth import get_user_model

User = get_user_model()

class MaterielBureauForm(forms.ModelForm):
    class Meta:
        model = MaterielBureau
        fields = [
            'code_inventaire', 'commande', 'ligne_commande', 'utilisateur',
            'statut', 'lieu_stockage', 'observation'
        ]
        widgets = {
            'code_inventaire': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'commande': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'ligne_commande': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'utilisateur': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'statut': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'lieu_stockage': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'observation': forms.
            Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les querysets
        self.fields['commande'].queryset = CommandeBureau.objects.all().order_by('-date_commande')
        self.fields['utilisateur'].queryset = User.objects.all().order_by('username')
        
        # Charger toutes les lignes de commande pour la validation
        self.fields['ligne_commande'].queryset = LigneCommandeBureau.objects.all().select_related('designation', 'description', 'commande')

    def clean(self):
        cleaned_data = super().clean()
        commande = cleaned_data.get('commande')
        ligne_commande = cleaned_data.get('ligne_commande')
        
        # Vérifier que la ligne de commande appartient à la commande sélectionnée
        if commande and ligne_commande:
            if ligne_commande.commande != commande:
                raise forms.ValidationError(
                    "La ligne de commande sélectionnée n'appartient pas à la commande choisie."
                )
        
        return cleaned_data 