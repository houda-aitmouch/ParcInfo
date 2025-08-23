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
        
        # Si c'est une modification (instance existante), charger les données
        if self.instance.pk:
            # Définir la valeur initiale pour type_demande
            self.fields['type_demande'].initial = self.instance.type_demande
            
            # Charger les désignations et descriptions selon la catégorie
            if self.instance.categorie == 'informatique':
                # Charger les désignations informatiques
                self.fields['designation_info'].queryset = DesignationInfo.objects.all()
                if self.instance.designation_info:
                    # Charger les descriptions pour la désignation sélectionnée
                    self.fields['description_info'].queryset = DescriptionInfo.objects.filter(
                        designation=self.instance.designation_info
                    )
                    # Définir la valeur initiale
                    self.fields['designation_info'].initial = self.instance.designation_info.id
                    if self.instance.description_info:
                        self.fields['description_info'].initial = self.instance.description_info.id
            elif self.instance.categorie == 'bureau':
                # Charger les désignations de bureau
                self.fields['designation_bureau'].queryset = DesignationBureau.objects.all()
                if self.instance.designation_bureau:
                    # Charger les descriptions pour la désignation sélectionnée
                    self.fields['description_bureau'].queryset = DescriptionBureau.objects.filter(
                        designation=self.instance.designation_bureau
                    )
                    # Définir la valeur initiale
                    self.fields['designation_bureau'].initial = self.instance.designation_bureau.id
                    if self.instance.description_bureau:
                        self.fields['description_bureau'].initial = self.instance.description_bureau.id
            
            # Charger les fournitures selon la catégorie
            if self.instance.type_article == 'fourniture':
                if self.instance.categorie == 'informatique':
                    self.fields['fourniture'].queryset = Fourniture.get_by_categorie('informatique')
                elif self.instance.categorie == 'bureau':
                    self.fields['fourniture'].queryset = Fourniture.get_by_categorie('bureautique')
                if self.instance.fourniture:
                    self.fields['fourniture'].initial = self.instance.fourniture.id
    
    def clean(self):
        cleaned_data = super().clean()
        categorie = cleaned_data.get('categorie')
        type_article = cleaned_data.get('type_article')
        type_demande = cleaned_data.get('type_demande')
        
        # Si c'est une modification (instance existante), préserver les valeurs existantes
        if self.instance and self.instance.pk:
            # Préserver les valeurs existantes si elles ne sont pas dans les données POST
            if 'type_demande' not in self.data and self.instance.type_demande:
                cleaned_data['type_demande'] = self.instance.type_demande
            if 'designation_info' not in self.data and self.instance.designation_info:
                cleaned_data['designation_info'] = self.instance.designation_info
            if 'description_info' not in self.data and self.instance.description_info:
                cleaned_data['description_info'] = self.instance.description_info
            if 'designation_bureau' not in self.data and self.instance.designation_bureau:
                cleaned_data['designation_bureau'] = self.instance.designation_bureau
            if 'description_bureau' not in self.data and self.instance.description_bureau:
                cleaned_data['description_bureau'] = self.instance.description_bureau
            if 'fourniture' not in self.data and self.instance.fourniture:
                cleaned_data['fourniture'] = self.instance.fourniture
        
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
    
 