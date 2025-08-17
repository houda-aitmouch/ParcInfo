from django import forms
from django.core.exceptions import ValidationError
from .models import DemandeEquipement, Fourniture
from apps.commande_informatique.models import Designation as DesignationInfo, Description as DescriptionInfo
from apps.commande_bureau.models import DesignationBureau, DescriptionBureau

class DemandeEquipementForm(forms.ModelForm):
    # Redéfinir les champs avec les choix explicites
    categorie = forms.ChoiceField(
        choices=DemandeEquipement.CATEGORIE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'id': 'id_categorie'
        })
    )
    
    type_article = forms.ChoiceField(
        choices=DemandeEquipement.TYPE_ARTICLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'id': 'id_type_article'
        })
    )
    
    type_demande = forms.ChoiceField(
        choices=DemandeEquipement.TYPE_DEMANDE_CHOICES,
        initial='nouveau',
        widget=forms.Select(attrs={
            'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'id': 'id_type_demande'
        })
    )
    
    class Meta:
        model = DemandeEquipement
        fields = [
            'categorie', 'type_article', 'type_demande', 
            'designation_info', 'description_info',
            'designation_bureau', 'description_bureau',
            'fourniture'
        ]
        widgets = {
            'designation_info': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'id': 'id_designation_info'
            }),
            'description_info': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'id': 'id_description_info'
            }),
            'designation_bureau': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'id': 'id_designation_bureau'
            }),
            'description_bureau': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'id': 'id_description_bureau'
            }),
            'fourniture': forms.Select(attrs={
                'class': 'form-select block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'id': 'id_fourniture'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir la valeur initiale pour type_demande
        if not self.instance.pk:  # Seulement pour les nouveaux formulaires
            self.fields['type_demande'].initial = 'nouveau'
        
        # Ajouter des classes CSS pour les champs conditionnels
        self.fields['designation_info'].widget.attrs['class'] += ' conditional-field'
        self.fields['description_info'].widget.attrs['class'] += ' conditional-field'
        self.fields['designation_bureau'].widget.attrs['class'] += ' conditional-field'
        self.fields['description_bureau'].widget.attrs['class'] += ' conditional-field'
        self.fields['fourniture'].widget.attrs['class'] += ' conditional-field'
    
    def clean(self):
        cleaned_data = super().clean()
        categorie = cleaned_data.get('categorie')
        type_article = cleaned_data.get('type_article')
        type_demande = cleaned_data.get('type_demande')
        
        # Validation pour les fournitures
        if type_article == 'fourniture':
            if type_demande != 'nouveau':
                raise ValidationError("Pour les fournitures, le type de demande doit être 'Nouveau'")
            
            # Vérifier que une fourniture est sélectionnée
            if not cleaned_data.get('fourniture'):
                raise ValidationError("La sélection d'une fourniture est obligatoire")
            
            # Vider les champs de désignation/description pour les fournitures
            cleaned_data['designation_info'] = None
            cleaned_data['description_info'] = None
            cleaned_data['designation_bureau'] = None
            cleaned_data['description_bureau'] = None
        
        # Validation pour les matériels
        elif type_article == 'materiel':
            # Vider le champ fourniture pour les matériels
            cleaned_data['fourniture'] = None
            
            if categorie == 'informatique':
                if not cleaned_data.get('designation_info'):
                    raise ValidationError("La désignation est obligatoire pour les matériels informatiques")
                if not cleaned_data.get('description_info'):
                    raise ValidationError("La description est obligatoire pour les matériels informatiques")
            elif categorie == 'bureau':
                if not cleaned_data.get('designation_bureau'):
                    raise ValidationError("La désignation est obligatoire pour les matériels de bureau")
                if not cleaned_data.get('description_bureau'):
                    raise ValidationError("La description est obligatoire pour les matériels de bureau")
        
        return cleaned_data
    
 