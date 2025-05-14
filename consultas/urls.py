from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    # URLs para Citas
    path('citas/', views.CitaListView.as_view(), name='lista_citas'),
    path('citas/crear/', views.CitaCreateView.as_view(), name='crear_cita'),
    path('mascota/<int:mascota_id>/cita/crear/', views.CitaCreateView.as_view(), name='crear_cita_mascota'),
    path('cita/<int:pk>/', views.CitaDetailView.as_view(), name='detalle_cita'),
    path('cita/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='editar_cita'),
    path('cita/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='eliminar_cita'),
    
    # URLs para Consultas
    path('cita/<int:cita_id>/consulta/crear/', views.ConsultaCreateView.as_view(), name='crear_consulta'),
    path('consulta/<int:pk>/', views.ConsultaDetailView.as_view(), name='detalle_consulta'),
    path('consulta/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='editar_consulta'),
    path('consulta/<int:pk>/eliminar/', views.ConsultaDeleteView.as_view(), name='eliminar_consulta'),
    
    # URL para Historia Clínica
    path('mascota/<int:mascota_id>/historia-clinica/', views.HistoriaClinicaView.as_view(), name='historia_clinica'),
]