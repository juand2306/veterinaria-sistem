from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard')
    template_name = 'usuarios/cambiar_password.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Contraseña cambiada correctamente')
        return super().form_valid(form)

@login_required
def dashboard(request):
    return render(request, 'usuarios/dashboard.html')