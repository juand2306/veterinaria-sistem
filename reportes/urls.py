from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='reportes_dashboard'),
    path('citas/', views.reporte_citas, name='reporte_citas'),
    path('vacunas/', views.reporte_vacunas, name='reporte_vacunas'),
    path('productos/', views.reporte_productos, name='reporte_productos'),
    path('eutanasias/', views.reporte_eutanasias, name='reporte_eutanasias'),
]