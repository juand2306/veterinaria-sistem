from django.urls import path
from . import views

urlpatterns = [
    # URLs para Vacunas
    path('vacunas/', views.VacunaListView.as_view(), name='vacuna-list'),
    path('vacunas/nueva/', views.VacunaCreateView.as_view(), name='vacuna-create'),
    path('vacunas/<int:pk>/editar/', views.VacunaUpdateView.as_view(), name='vacuna-update'),
    path('vacunas/<int:pk>/eliminar/', views.VacunaDeleteView.as_view(), name='vacuna-delete'),
    
    # URLs para Vacunas Aplicadas
    path('vacunas/aplicar/<int:mascota_id>/', views.VacunaAplicadaCreateView.as_view(), name='vacuna-aplicada-create'),
    path('vacunas/aplicada/<int:pk>/editar/', views.VacunaAplicadaUpdateView.as_view(), name='vacuna-aplicada-update'),
    path('vacunas/aplicada/<int:pk>/eliminar/', views.VacunaAplicadaDeleteView.as_view(), name='vacuna-aplicada-delete'),
    
    # URLs para Productos
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto-delete'),
    
    # URLs para Productos Aplicados
    path('productos/aplicar/<int:mascota_id>/', views.ProductoAplicadoCreateView.as_view(), name='producto-aplicado-create'),
    path('productos/aplicado/<int:pk>/editar/', views.ProductoAplicadoUpdateView.as_view(), name='producto-aplicada-update'),
    path('productos/aplicado/<int:pk>/eliminar/', views.ProductoAplicadoDeleteView.as_view(), name='producto-aplicada-delete'),
]