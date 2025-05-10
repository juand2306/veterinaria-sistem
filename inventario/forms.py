from django import forms
from .models import Vacuna, VacunaAplicada, Producto, ProductoAplicado

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class VacunaAplicadaForm(forms.ModelForm):
    class Meta:
        model = VacunaAplicada
        fields = ['mascota', 'vacuna', 'fecha_aplicacion', 'fecha_proxima', 'observaciones']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_proxima': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'tipo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoAplicadoForm(forms.ModelForm):
    class Meta:
        model = ProductoAplicado
        fields = ['mascota', 'producto', 'fecha_aplicacion', 'fecha_proxima', 'observaciones']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_proxima': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }