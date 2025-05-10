from django import forms
from .models import Especie, Raza

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = ['nombre', 'especie', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }