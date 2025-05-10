from django import forms
from .models import Cliente, Mascota, ImagenDiagnostica
from configuracion.models import Especie, Raza

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay una especie seleccionada, filtrar las razas
        if 'especie' in self.data:
            try:
                especie_id = int(self.data.get('especie'))
                self.fields['raza'].queryset = Raza.objects.filter(especie_id=especie_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.especie:
            self.fields['raza'].queryset = Raza.objects.filter(especie=self.instance.especie).order_by('nombre')
        else:
            self.fields['raza'].queryset = Raza.objects.none()

class ImagenDiagnosticaForm(forms.ModelForm):
    class Meta:
        model = ImagenDiagnostica
        fields = ['archivo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }