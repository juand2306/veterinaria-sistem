from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView


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