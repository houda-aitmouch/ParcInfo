from django import forms
from .models import MaterielInformatique
from apps.commande_informatique.models import Commande, LigneCommande
from apps.materiel_bureautique.models import MaterielBureau
from django.contrib.auth import get_user_model

User = get_user_model()

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
        widgets = {
            'numero_serie': forms.TextInput(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'code_inventaire': forms.TextInput(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'commande': forms.Select(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'ligne_commande': forms.Select(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'utilisateur': forms.Select(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-green-500/30 focus:border-green-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'statut': forms.Select(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-indigo-500/30 focus:border-indigo-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'lieu_stockage': forms.Select(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-purple-500/30 focus:border-purple-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md'}),
            'observation': forms.Textarea(attrs={'class': 'w-full border-2 border-gray-300 rounded-xl px-5 py-4 bg-white focus:outline-none focus:ring-3 focus:ring-teal-500/30 focus:border-teal-500 transition-all duration-300 text-gray-900 font-medium shadow-sm hover:shadow-md min-h-[100px] resize-y', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les querysets
        self.fields['commande'].queryset = Commande.objects.all().order_by('-date_commande')
        self.fields['utilisateur'].queryset = User.objects.all().order_by('username')
        
        # Charger toutes les lignes de commande pour la validation
        self.fields['ligne_commande'].queryset = LigneCommande.objects.all().select_related('designation', 'description', 'commande')

    def clean_code_inventaire(self):
        """Valider l'unicité globale du code d'inventaire"""
        code_inventaire = self.cleaned_data.get('code_inventaire')
        
        if code_inventaire:
            # Vérifier l'unicité dans MaterielInformatique
            queryset_info = MaterielInformatique.objects.filter(code_inventaire=code_inventaire)
            if self.instance.pk:
                queryset_info = queryset_info.exclude(pk=self.instance.pk)
            
            if queryset_info.exists():
                raise forms.ValidationError(
                    f"Le code d'inventaire '{code_inventaire}' existe déjà dans les matériels informatiques."
                )
            
            # Vérifier l'unicité dans MaterielBureau
            if MaterielBureau.objects.filter(code_inventaire=code_inventaire).exists():
                raise forms.ValidationError(
                    f"Le code d'inventaire '{code_inventaire}' existe déjà dans les matériels de bureau."
                )
        
        return code_inventaire

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
        
        # Vérifier la quantité maximale
        if ligne_commande:
            deja_ajoutes = MaterielInformatique.objects.filter(ligne_commande=ligne_commande).count()
            if self.instance.pk:
                # Exclure l'instance en cours de modification
                deja_ajoutes = deja_ajoutes - 1
            if deja_ajoutes >= ligne_commande.quantite:
                raise forms.ValidationError(
                    f"Vous ne pouvez pas ajouter plus de {ligne_commande.quantite} matériels pour cette commande (quantité maximale atteinte). Veuillez augmenter la quantité dans la commande si besoin."
                )
        return cleaned_data