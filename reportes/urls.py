from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    #Check
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('citas/', views.ReporteCitasView.as_view(), name='reporte_citas'),
    path('vacunas/', views.ReporteVacunasView.as_view(), name='reporte_vacunas'),
    path('productos/', views.ReporteProductosView.as_view(), name='reporte_productos'),
    path('eutanasias/', views.ReporteEutanasiasView.as_view(), name='reporte_eutanasias'),
]