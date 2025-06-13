from django import forms
from .models import AccesoCliente


class LoginPortalForm(forms.Form):
    """Formulario de login para clientes del portal"""
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'autocomplete': 'username'
        }),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contrasena',
            'autocomplete': 'current-password'
        }),
        label='Contraseña'
    )


class AccesoClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Determinar si es edición o creación
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Si es edición, hacer los campos de contraseña opcionales
        if self.is_edit:
            self.fields['password'].required = False
            self.fields['confirmar_password'].required = False
            self.fields['password'].help_text = 'Dejar en blanco para mantener la contraseña actual'
            self.fields['confirmar_password'].help_text = 'Solo necesario si cambias la contraseña'
            
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese contraseña'
        }),
        label='Contraseña',
        help_text='Mínimo 6 caracteres'
        # NO agregar required=False aquí
    )

    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme contraseña'
        }),
        label='Confirmar Contraseña'
        # NO agregar required=False aquí
    )
    
    class Meta:
        model = AccesoCliente
        fields = ['username', 'password', 'activo']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario único'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_confirmar_password(self):
        password = self.cleaned_data.get('password')
        confirmar_password = self.cleaned_data.get('confirmar_password')
        
        # Solo validar si se está intentando cambiar la contraseña
        if password or confirmar_password:
            if password != confirmar_password:
                raise forms.ValidationError('Las contraseñas no coinciden')
        
        return confirmar_password
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres')
        return password