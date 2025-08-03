from django import forms
from .models import Livraison


class LivraisonForm(forms.ModelForm):
    """Formulaire pour créer/modifier une livraison"""
    
    class Meta:
        model = Livraison
        fields = [
            'commande_informatique', 'commande_bureau', 'date_livraison_prevue',
            'date_livraison_effective', 'statut_livraison', 'conforme', 
            'pv_reception_recu', 'notes'
        ]
        widgets = {
            'date_livraison_prevue': forms.DateInput(attrs={'type': 'date'}),
            'date_livraison_effective': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les widgets
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Rendre les champs de commande optionnels
        self.fields['commande_informatique'].required = False
        self.fields['commande_bureau'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        commande_informatique = cleaned_data.get('commande_informatique')
        commande_bureau = cleaned_data.get('commande_bureau')
        
        # Vérifier qu'au moins une commande est sélectionnée
        if not commande_informatique and not commande_bureau:
            raise forms.ValidationError("Vous devez sélectionner au moins une commande (informatique ou bureau).")
        
        # Vérifier qu'une seule commande est sélectionnée
        if commande_informatique and commande_bureau:
            raise forms.ValidationError("Vous ne pouvez sélectionner qu'une seule commande à la fois.")
        
        return cleaned_data


class RechercheLivraisonForm(forms.Form):
    """Formulaire de recherche de livraisons"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par numéro de commande, fournisseur...'
        })
    )
    
    type_commande = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Livraison.TYPE_COMMANDE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    statut_livraison = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Livraison.STATUT_LIVRAISON_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    conforme = forms.ChoiceField(
        choices=[
            ('', 'Toutes'),
            ('True', 'Conformes'),
            ('False', 'Non conformes')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pv_reception = forms.ChoiceField(
        choices=[
            ('', 'Tous'),
            ('True', 'PV reçus'),
            ('False', 'PV non reçus')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class NouvelleLivraisonForm(forms.Form):
    """Formulaire personnalisé pour créer une nouvelle livraison"""
    
    TYPE_COMMANDE_CHOICES = [
        ('', 'Sélectionner un type'),
        ('informatique', 'Commande Informatique'),
        ('bureau', 'Commande Bureau'),
    ]
    
    STATUT_LIVRAISON_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('retardee', 'Retardée'),
        ('annulee', 'Annulée'),
    ]
    
    type_commande = forms.ChoiceField(
        choices=TYPE_COMMANDE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'type-commande'
        })
    )
    
    commande_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput(attrs={
            'id': 'commande-select'
        })
    )
    
    date_livraison_prevue = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_livraison_effective = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    statut_livraison = forms.ChoiceField(
        choices=STATUT_LIVRAISON_CHOICES,
        initial='en_attente',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    conforme = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    pv_reception_recu = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Notes supplémentaires sur la livraison...'
        })
    )
    
    def clean_commande_id(self):
        """Validation personnalisée pour commande_id"""
        commande_id = self.cleaned_data.get('commande_id')
        type_commande = self.cleaned_data.get('type_commande')
        
        if not commande_id:
            raise forms.ValidationError("Veuillez sélectionner une commande.")
        
        # Vérifier que la commande existe
        try:
            if type_commande == 'informatique':
                from apps.commande_informatique.models import Commande
                Commande.objects.get(id=commande_id)
            elif type_commande == 'bureau':
                from apps.commande_bureau.models import CommandeBureau
                CommandeBureau.objects.get(id=commande_id)
            else:
                raise forms.ValidationError("Type de commande invalide.")
        except Exception:
            raise forms.ValidationError("La commande sélectionnée n'existe pas.")
        
        return commande_id 


class ModifierLivraisonForm(forms.Form):
    """Formulaire pour modifier une livraison existante (sans validation des champs de commande)"""
    
    STATUT_LIVRAISON_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('retardee', 'Retardée'),
        ('annulee', 'Annulée'),
    ]
    
    # Champs en lecture seule (pas de validation)
    type_commande = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    commande_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    date_livraison_prevue = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_livraison_effective = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    statut_livraison = forms.ChoiceField(
        choices=STATUT_LIVRAISON_CHOICES,
        initial='en_attente',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    conforme = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    pv_reception_recu = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Notes supplémentaires sur la livraison...'
        })
    ) 