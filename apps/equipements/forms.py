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
        }



class MaterielAffectationForm(forms.ModelForm):
    affecte_a = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Affecté à")

    class Meta:
        model = Materiel
        fields = ['affecte_a']