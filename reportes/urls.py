from django.urls import path
from . import views

urlpatterns = [
    path('citas/', views.ReporteCitasView.as_view(), name='reporte-citas'),
    path('vacunas/', views.ReporteVacunasView.as_view(), name='reporte-vacunas'),
    path('productos/', views.ReporteProductosView.as_view(), name='reporte-productos'),
    path('eutanasias/', views.ReporteEutanasiasView.as_view(), name='reporte-eutanasias'),
]