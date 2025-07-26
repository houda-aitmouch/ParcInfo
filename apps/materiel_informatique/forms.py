from django import forms
from .models import MaterielInformatique

class MaterielInformatiqueForm(forms.ModelForm):
    class Meta:
        model = MaterielInformatique
        fields = [
            'commande',
            'ligne_commande',
            'numero_serie',
            'code_inventaire',
            'utilisateur',
            'statut',
            'public',
            'lieu_stockage',
            'observation',
        ]

    def clean(self):
        cleaned_data = super().clean()
        ligne = cleaned_data.get('ligne_commande')
        if ligne:
            deja_ajoutes = MaterielInformatique.objects.filter(ligne_commande=ligne).count()
            if self.instance.pk:
                # Exclure l'instance en cours de modification
                deja_ajoutes = deja_ajoutes - 1
            if deja_ajoutes >= ligne.quantite:
                raise forms.ValidationError(
                    f"Vous ne pouvez pas ajouter plus de {ligne.quantite} matériels pour cette commande (quantité maximale atteinte). Veuillez augmenter la quantité dans la commande si besoin."
                )
        return cleaned_data