from django.urls import path
from . import views

app_name = 'configuracion'
#Completa 99%
urlpatterns = [
    # URLs para Especies #Check
    path('especies/', views.EspecieListView.as_view(), name='lista_especies'),
    path('especies/crear/', views.EspecieCreateView.as_view(), name='crear_especie'), 
    path('especie/<int:pk>/editar/', views.EspecieUpdateView.as_view(), name='editar_especie'), 
    path('especie/<int:pk>/eliminar/', views.EspecieDeleteView.as_view(), name='eliminar_especie'),
    
    # URLs para Razas #Check
    path('razas/', views.RazaListView.as_view(), name='lista_razas'),
    path('razas/crear/', views.RazaCreateView.as_view(), name='crear_raza'),
    path('raza/<int:pk>/editar/', views.RazaUpdateView.as_view(), name='editar_raza'), 
    path('raza/<int:pk>/eliminar/', views.RazaDeleteView.as_view(), name='eliminar_raza'),
]