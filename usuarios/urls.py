from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('cambiar-password/', views.CustomPasswordChangeView.as_view(), name='cambiar_password'),
    path('perfil/', views.PerfilUsuarioView.as_view(), name='perfil'),
    path('configurar-cuenta/', views.ConfigurarCuentaView.as_view(), name='configurar_cuenta'), #Falla
]