from django import forms
from .models import Vacuna, VacunaAplicada, Producto, ProductoAplicado
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'nombre',
            'descripcion',
            Submit('submit', 'Guardar')
        )

class VacunaAplicadaForm(forms.ModelForm):
    class Meta:
        model = VacunaAplicada
        fields = ['mascota', 'vacuna', 'fecha_aplicacion', 'fecha_proxima', 'observaciones']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_proxima': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
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
            'vacuna',
            Row(
                Column('fecha_aplicacion', css_class='form-group col-md-6 mb-0'),
                Column('fecha_proxima', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observaciones',
            Submit('submit', 'Guardar')
        )

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'tipo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'nombre',
            'tipo',
            'descripcion',
            Submit('submit', 'Guardar')
        )

class ProductoAplicadoForm(forms.ModelForm):
    class Meta:
        model = ProductoAplicado
        fields = ['mascota', 'producto', 'fecha_aplicacion', 'fecha_proxima', 'observaciones']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_proxima': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
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
            'producto',
            Row(
                Column('fecha_aplicacion', css_class='form-group col-md-6 mb-0'),
                Column('fecha_proxima', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observaciones',
            Submit('submit', 'Guardar')
        )