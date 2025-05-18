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
from .models import PerfilUsuario


class CustomUserForm(forms.ModelForm):
    """Formulario personalizado para editar datos del usuario"""
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para el perfil del usuario"""
    telefono = forms.CharField(
        max_length=15,
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cargo = forms.CharField(
        max_length=100,
        required=False,
        label='Cargo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'cargo']


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f"Bienvenido/a {form.get_user().username}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('reportes:dashboard')


class CustomLogoutView(LogoutView):
    next_page = 'usuarios:login'
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Has cerrado sesión exitosamente.")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuarios/cambiar_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('reportes:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido actualizada exitosamente.")
        return super().form_valid(form)


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    """Vista para mostrar el perfil del usuario"""
    template_name = 'usuarios/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            context['perfil'] = self.request.user.perfil
        except PerfilUsuario.DoesNotExist:
            # Crear perfil si no existe
            context['perfil'] = PerfilUsuario.objects.create(user=self.request.user)
        return context


class ConfigurarCuentaView(LoginRequiredMixin, FormView):
    """Vista para configurar la cuenta del usuario"""
    template_name = 'usuarios/configurar_cuenta.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
        })
        try:
            perfil = self.request.user.perfil
            initial.update({
                'telefono': perfil.telefono,
                'cargo': perfil.cargo,
            })
        except PerfilUsuario.DoesNotExist:
            pass
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'user_form'):
            self.user_form = CustomUserForm(initial=self.get_initial())
        if not hasattr(self, 'perfil_form'):
            self.perfil_form = PerfilUsuarioForm(initial=self.get_initial())
        
        context['user_form'] = self.user_form
        context['perfil_form'] = self.perfil_form
        return context
    
    def post(self, request, *args, **kwargs):
        self.user_form = CustomUserForm(request.POST, instance=request.user)
        
        # Obtener o crear perfil
        try:
            perfil = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario.objects.create(user=request.user)
        
        self.perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        
        if self.user_form.is_valid() and self.perfil_form.is_valid():
            self.user_form.save()
            self.perfil_form.save()
            messages.success(request, "Tu información ha sido actualizada exitosamente.")
            return redirect('usuarios:perfil')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            return self.render_to_response(self.get_context_data())