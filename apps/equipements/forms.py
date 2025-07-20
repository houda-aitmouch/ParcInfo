from django import forms
from .models import Equipement, Materiel, User

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = '__all__'
        widgets = {
            'date_garantie': forms.DateInput(attrs={'type': 'date'}),
            'date_service': forms.DateInput(attrs={'type': 'date'}),
            'reparation': forms.CheckboxInput(),
            'is_public': forms.CheckboxInput(),
        }  # <-- Parenthèse fermante ajoutée ici

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = '__all__'
        widgets = {
            'date_service': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date_service': 'Date de mise en service',
        }

class MaterielAffectationForm(forms.ModelForm):
    affecte_a = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Affecté à",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Materiel
        fields = ['affecte_a', 'date_service']
        widgets = {
            'date_service': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'date_service': 'Date de mise en service',
        }