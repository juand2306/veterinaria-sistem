from django import forms
from .models import Especie, Raza

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la especie'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional de la especie'
            }),
        }
        labels = {
            'nombre': 'Nombre de la especie',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el campo nombre sea requerido
        self.fields['nombre'].required = True
        # Personalizar mensajes de error
        self.fields['nombre'].error_messages = {
            'required': 'El nombre de la especie es obligatorio.',
            'unique': 'Ya existe una especie con este nombre.',
        }

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = ['nombre', 'especie', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la raza'
            }),
            'especie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional de la raza'
            }),
        }
        labels = {
            'nombre': 'Nombre de la raza',
            'especie': 'Especie',
            'descripcion': 'Descripción',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos sean requeridos
        self.fields['nombre'].required = True
        self.fields['especie'].required = True
        
        # Personalizar mensajes de error
        self.fields['nombre'].error_messages = {
            'required': 'El nombre de la raza es obligatorio.',
        }
        self.fields['especie'].error_messages = {
            'required': 'Debe seleccionar una especie.',
        }
        
        # Mejorar el select de especies
        self.fields['especie'].empty_label = "-- Seleccione una especie --"
        
        # Verificar si hay especies disponibles
        if not self.fields['especie'].queryset.exists():
            self.fields['especie'].widget.attrs['disabled'] = True