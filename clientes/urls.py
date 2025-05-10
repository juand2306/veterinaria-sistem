from django.urls import path
from . import views

urlpatterns = [
    # Rutas para clientes
    path('', views.lista_clientes, name='lista_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('<int:pk>/', views.detalle_cliente, name='detalle_cliente'),
    path('<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Rutas para mascotas
    path('mascota/crear/<int:cliente_id>/', views.crear_mascota, name='crear_mascota'),
    path('mascota/<int:pk>/', views.detalle_mascota, name='detalle_mascota'),
    path('mascota/<int:pk>/editar/', views.editar_mascota, name='editar_mascota'),
    path('mascota/<int:pk>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),
    
    # Ajax para cargar razas
    path('cargar-razas/', views.cargar_razas, name='cargar_razas'),
    
    # Imágenes diagnósticas
    path('mascota/<int:mascota_id>/agregar-imagen/', views.agregar_imagen, name='agregar_imagen'),
]