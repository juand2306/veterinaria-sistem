from django.urls import path
from . import views

app_name = 'portal_cliente'

urlpatterns = [
    # URLs del portal de clientes
    path('portal/login/', views.PortalLoginView.as_view(), name='login'), #check
    path('portal/dashboard/', views.PortalDashboardView.as_view(), name='dashboard'), #check
    path('portal/mascota/<int:mascota_id>/historia/', views.PortalHistoriaClinicaView.as_view(), name='historia_clinica'), #check
    path('portal/logout/', views.PortalLogoutView.as_view(), name='logout'),
    path('portal/mascota/<int:mascota_id>/historia/imprimir/v2/', views.PortalHistoriaClinicaImprimibleView.as_view(), name='historia_clinica_imprimible_v3'),    

    
    # URLs para administración del portal (personal de veterinaria)
    path('admin-portal/lista-accesos/', views.ListaAccesosView.as_view(), name='lista_accesos'), #check
    path('admin-portal/crear-acceso/<int:cliente_id>/', views.CrearAccesoClienteView.as_view(), name='crear_acceso'),#check
    path('admin-portal/editar-acceso/<int:acceso_id>/', views.EditarAccesoClienteView.as_view(), name='editar_acceso'), #Check
    path('admin-portal/eliminar-acceso/<int:acceso_id>/', views.EliminarAccesoClienteView.as_view(), name='eliminar_acceso'), #check
]