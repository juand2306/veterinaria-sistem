from django.urls import path
from . import views

urlpatterns = [
    # URLs para Clientes
    path('', views.ClienteListView.as_view(), name='cliente-list'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
    
    # URLs para Mascotas
    path('mascota/nueva/<int:cliente_id>/', views.MascotaCreateView.as_view(), name='mascota-create'),
    path('mascota/<int:pk>/', views.MascotaDetailView.as_view(), name='mascota-detail'),
    path('mascota/<int:pk>/editar/', views.MascotaUpdateView.as_view(), name='mascota-update'),
    path('mascota/<int:pk>/eliminar/', views.MascotaDeleteView.as_view(), name='mascota-delete'),
    
    # URLs para APIs AJAX
    path('api/razas/', views.get_razas_by_especie, name='get-razas'),
]