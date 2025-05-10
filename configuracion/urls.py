from django.urls import path
from . import views

urlpatterns = [
    # Rutas para especies
    path('especies/', views.lista_especies, name='lista_especies'),
    path('especies/crear/', views.crear_especie, name='crear_especie'),
    path('especies/<int:pk>/editar/', views.editar_especie, name='editar_especie'),
    path('especies/<int:pk>/eliminar/', views.eliminar_especie, name='eliminar_especie'),
    
    # Rutas para razas
    path('razas/', views.lista_razas, name='lista_razas'),
    path('razas/crear/', views.crear_raza, name='crear_raza'),
    path('razas/<int:pk>/editar/', views.editar_raza, name='editar_raza'),
    path('razas/<int:pk>/eliminar/', views.eliminar_raza, name='eliminar_raza'),
]