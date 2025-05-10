from django.urls import path
from . import views

urlpatterns = [
    # Rutas para citas
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/crear/<int:mascota_id>/', views.crear_cita, name='crear_cita_mascota'),
    path('citas/<int:pk>/', views.detalle_cita, name='detalle_cita'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:pk>/eliminar/', views.eliminar_cita, name='eliminar_cita'),
    
    # Rutas para consultas
    path('citas/<int:cita_id>/registrar-consulta/', views.registrar_consulta, name='registrar_consulta'),
    path('consultas/<int:pk>/editar/', views.editar_consulta, name='editar_consulta'),
]