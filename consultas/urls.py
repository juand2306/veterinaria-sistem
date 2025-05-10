from django.urls import path
from . import views

urlpatterns = [
    # URLs para Citas
    path('citas/', views.CitaListView.as_view(), name='cita-list'),
    path('citas/nueva/', views.CitaCreateView.as_view(), name='cita-create'),
    path('citas/nueva/<int:mascota_id>/', views.CitaCreateView.as_view(), name='cita-create-mascota'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='cita-detail'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita-update'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita-delete'),
    
    # URLs para Consultas
    path('citas/<int:cita_id>/consulta/nueva/', views.ConsultaCreateView.as_view(), name='consulta-create'),
    path('consulta/<int:pk>/', views.ConsultaDetailView.as_view(), name='consulta-detail'),
    path('consulta/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='consulta-update'),
    
    # URLs para Imágenes Diagnósticas
    path('imagenes/nueva/<int:mascota_id>/', views.ImagenDiagnosticaCreateView.as_view(), name='imagen-create'),
]