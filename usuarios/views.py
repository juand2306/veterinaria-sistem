from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import PerfilUsuario


class CustomUserForm(forms.ModelForm):
    """Formulario personalizado para editar datos del usuario"""
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido'
        })
    )
    email = forms.EmailField(
        required=False,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que no exista otro usuario con el mismo email (excluyendo el actual)
            existing_user = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email


class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para el perfil del usuario"""
    telefono = forms.CharField(
        max_length=15,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 123-456-7890'
        })
    )
    cargo = forms.CharField(
        max_length=100,
        required=False,
        label='Cargo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Veterinario Principal'
        })
    )
    
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'cargo']
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Limpiar el teléfono de caracteres no numéricos para validación
            numeros_solo = re.sub(r'\D', '', telefono)
            if len(numeros_solo) < 7 or len(numeros_solo) > 15:
                raise ValidationError("El teléfono debe tener entre 7 y 15 números.")
        return telefono


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f"¡Bienvenido/a {form.get_user().get_full_name() or form.get_user().username}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('reportes:dashboard')


class CustomLogoutView(LogoutView):
    next_page = 'usuarios:login'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, f"Hasta luego, {request.user.get_full_name() or request.user.username}. Has cerrado sesión exitosamente.")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuarios/cambiar_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('usuarios:perfil')
    
    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido actualizada exitosamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    """Vista para mostrar el perfil del usuario"""
    template_name = 'usuarios/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
        # Obtener o crear perfil si no existe
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.request.user)
        context['perfil'] = perfil
        
        # Si se creó un nuevo perfil, informar al usuario
        if created:
            messages.info(self.request, "Se ha creado tu perfil. Puedes actualizarlo con tu información personal.")
        
        return context


class ConfigurarCuentaView(LoginRequiredMixin, TemplateView):
    """Vista para configurar la cuenta del usuario"""
    template_name = 'usuarios/configurar_cuenta.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener o crear perfil
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.request.user)
        
        # Crear formularios
        context['user_form'] = CustomUserForm(instance=self.request.user)
        context['perfil_form'] = PerfilUsuarioForm(instance=perfil)
        
        return context
    
    def post(self, request, *args, **kwargs):
        # Obtener o crear perfil
        perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
        
        # Crear formularios con datos del POST
        user_form = CustomUserForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        
        # Validar ambos formularios
        if user_form.is_valid() and perfil_form.is_valid():
            # Guardar información del usuario
            user = user_form.save()
            
            # Guardar información del perfil
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            
            messages.success(request, "Tu información ha sido actualizada exitosamente.")
            return redirect('usuarios:perfil')
        else:
            # Si hay errores, mostrar mensaje y renderizar formulario con errores
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            
            # Preparar context con formularios que contienen errores
            context = self.get_context_data(**kwargs)
            context['user_form'] = user_form
            context['perfil_form'] = perfil_form
            
            return self.render_to_response(context)