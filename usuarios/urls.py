from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cambiar-password/', auth_views.PasswordChangeView.as_view( template_name='usuarios/password_change.html', success_url='/usuarios/password-success/' ), name='password_change'),
    path('password-success/', auth_views.PasswordChangeDoneView.as_view( template_name='usuarios/password_change_done.html' ), name='password_change_done'),
]