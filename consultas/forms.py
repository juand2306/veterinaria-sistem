from django import forms
from .models import Cita, Consulta, ImagenDiagnostica
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mascota', 'fecha', 'motivo', 'programada']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Si se proporciona una mascota en la instancia, pre-establecerla
        if 'initial' in kwargs and 'mascota' in kwargs['initial']:
            self.fields['mascota'].initial = kwargs['initial']['mascota']
            self.fields['mascota'].widget.attrs['readonly'] = True
        
        self.helper.layout = Layout(
            'mascota',
            Row(
                Column('fecha', css_class='form-group col-md-6 mb-0'),
                Column('programada', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'motivo',
            Submit('submit', 'Guardar')
        )
    
    def clean_mascota(self):
        mascota = self.cleaned_data.get('mascota')
        if not mascota.activa:
            raise forms.ValidationError("No se pueden agendar citas para mascotas inactivas.")
        return mascota

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['diagnostico', 'tratamiento', 'notas', 'es_eutanasia']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'diagnostico',
            'tratamiento',
            'notas',
            'es_eutanasia',
            Submit('submit', 'Guardar')
        )

class ImagenDiagnosticaForm(forms.ModelForm):
    class Meta:
        model = ImagenDiagnostica
        fields = ['mascota', 'archivo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe la imagen diagnóstica...'}),
            'archivo': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        
        # Si se proporciona una mascota en initial, pre-establecerla y ocultarla
        if 'initial' in kwargs and 'mascota' in kwargs['initial']:
            self.fields['mascota'].initial = kwargs['initial']['mascota']
            self.fields['mascota'].widget = forms.HiddenInput()
        
        # Mejorar etiquetas y placeholder
        self.fields['archivo'].label = 'Imagen diagnóstica'
        self.fields['descripcion'].label = 'Descripción'
        
        self.helper.layout = Layout(
            'mascota',
            'archivo',
            'descripcion',
            Submit('submit', 'Guardar Imagen', css_class='btn btn-primary')
        )