from django.urls import path
from . import views

urlpatterns = [
    # Rutas para vacunas
    path('vacunas/', views.lista_vacunas, name='lista_vacunas'),
    path('vacunas/crear/', views.crear_vacuna, name='crear_vacuna'),
    path('vacunas/<int:pk>/editar/', views.editar_vacuna, name='editar_vacuna'),
    path('vacunas/<int:pk>/eliminar/', views.eliminar_vacuna, name='eliminar_vacuna'),
    
    # Rutas para vacunas aplicadas
    path('vacunas/aplicar/', views.aplicar_vacuna, name='aplicar_vacuna'),
    path('vacunas/aplicar/<int:mascota_id>/', views.aplicar_vacuna, name='aplicar_vacuna_mascota'),
    path('vacunas/aplicadas/', views.lista_vacunas_aplicadas, name='lista_vacunas_aplicadas'),
    
    # Rutas para productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    # Rutas para productos aplicados
    path('productos/aplicar/', views.aplicar_producto, name='aplicar_producto'),
    path('productos/aplicar/<int:mascota_id>/', views.aplicar_producto, name='aplicar_producto_mascota'),
    path('productos/aplicados/', views.lista_productos_aplicados, name='lista_productos_aplicados'),
]