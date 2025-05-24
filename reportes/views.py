from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta

from consultas.models import Cita, Consulta
from inventario.models import VacunaAplicada, ProductoAplicado
from clientes.models import Mascota


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fecha actual
        hoy = timezone.now().date()
        
        # Citas para hoy
        context['citas_hoy'] = Cita.objects.filter(fecha__date=hoy).count()
        
        # Citas para mañana
        manana = hoy + timedelta(days=1)
        context['citas_manana'] = Cita.objects.filter(fecha__date=manana).count()
        
        # Citas para esta semana (restantes)
        inicio_semana = hoy
        fin_semana = hoy + timedelta(days=(6 - hoy.weekday()))
        context['citas_semana'] = Cita.objects.filter(
            fecha__date__gt=hoy,
            fecha__date__lte=fin_semana
        ).count()
        
        # Vacunas próximas a vencer (en los próximos 7 días)
        prox_semana = hoy + timedelta(days=7)
        context['vacunas_proximas'] = VacunaAplicada.objects.filter(
            fecha_proxima__gte=hoy,
            fecha_proxima__lte=prox_semana
        ).count()
        
        # Antiparasitarios próximos a vencer
        context['antiparasitarios_proximos'] = ProductoAplicado.objects.filter(
            fecha_proxima__gte=hoy,
            fecha_proxima__lte=prox_semana
        ).count()
        
        # Total de mascotas activas
        context['total_mascotas'] = Mascota.objects.filter(activa=True).count()
        
        return context


class ReporteCitasView(LoginRequiredMixin, View):
    template_name = 'reportes/reporte_citas.html'
    
    def get(self, request):
        # Obtener fechas del formulario
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')
        
        # Calcular fechas por defecto (mes actual)
        hoy = timezone.now().date()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Usar fechas del formulario o fechas por defecto
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            except ValueError:
                # Si hay error en las fechas, usar fechas por defecto
                fecha_inicio = primer_dia_mes
                fecha_fin = ultimo_dia_mes
        else:
            # Si no hay fechas en el formulario, usar fechas por defecto
            fecha_inicio = primer_dia_mes
            fecha_fin = ultimo_dia_mes
        
        # Obtener citas en el rango de fechas (siempre se ejecuta)
        citas = Cita.objects.filter(
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        ).select_related('mascota__cliente').order_by('fecha')
        
        return render(request, self.template_name, {
            'citas': citas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_citas': citas.count(),
            'es_filtro_defecto': not (fecha_inicio_str and fecha_fin_str),  # Para mostrar un mensaje informativo
        })


class ReporteVacunasView(LoginRequiredMixin, View):
    template_name = 'reportes/reporte_vacunas.html'
    
    def get(self, request):
        # Obtener fechas del formulario
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')
        
        # Calcular fechas por defecto (mes actual)
        hoy = timezone.now().date()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Usar fechas del formulario o fechas por defecto
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            except ValueError:
                # Si hay error en las fechas, usar fechas por defecto
                fecha_inicio = primer_dia_mes
                fecha_fin = ultimo_dia_mes
        else:
            # Si no hay fechas en el formulario, usar fechas por defecto
            fecha_inicio = primer_dia_mes
            fecha_fin = ultimo_dia_mes
        
        # Obtener vacunas aplicadas en el rango de fechas con select_related para optimizar
        vacunas = VacunaAplicada.objects.filter(
            fecha_aplicacion__gte=fecha_inicio,
            fecha_aplicacion__lte=fecha_fin
        ).select_related(
            'vacuna', 
            'mascota__cliente'
        ).order_by('-fecha_aplicacion')
        
        # Estadísticas por tipo de vacuna
        stats_vacunas = VacunaAplicada.objects.filter(
            fecha_aplicacion__gte=fecha_inicio,
            fecha_aplicacion__lte=fecha_fin
        ).values('vacuna__nombre').annotate(total=Count('id')).order_by('-total')
        
        return render(request, self.template_name, {
            'vacunas': vacunas,
            'stats_vacunas': stats_vacunas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_vacunas': vacunas.count(),
            'es_filtro_defecto': not (fecha_inicio_str and fecha_fin_str),  # Para mostrar un mensaje informativo
        })


class ReporteProductosView(LoginRequiredMixin, View):
    template_name = 'reportes/reporte_productos.html'
    
    def get(self, request):
        # Obtener fechas del formulario
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')
        
        # Calcular fechas por defecto (mes actual)
        hoy = timezone.now().date()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Usar fechas del formulario o fechas por defecto
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            except ValueError:
                # Si hay error en las fechas, usar fechas por defecto
                fecha_inicio = primer_dia_mes
                fecha_fin = ultimo_dia_mes
        else:
            # Si no hay fechas en el formulario, usar fechas por defecto
            fecha_inicio = primer_dia_mes
            fecha_fin = ultimo_dia_mes
        
        # Obtener productos aplicados en el rango de fechas (siempre se ejecuta)
        # Removido __date porque fecha_aplicacion ya es DateField
        productos = ProductoAplicado.objects.filter(
            fecha_aplicacion__gte=fecha_inicio,
            fecha_aplicacion__lte=fecha_fin
        ).select_related('producto', 'mascota__cliente').order_by('-fecha_aplicacion')
        
        # Estadísticas por tipo de producto
        stats_productos = ProductoAplicado.objects.filter(
            fecha_aplicacion__gte=fecha_inicio,
            fecha_aplicacion__lte=fecha_fin
        ).values('producto__nombre', 'producto__tipo').annotate(total=Count('id')).order_by('-total')
        
        return render(request, self.template_name, {
            'productos': productos,
            'stats_productos': stats_productos,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_productos': productos.count(),
            'es_filtro_defecto': not (fecha_inicio_str and fecha_fin_str),  # Para mostrar un mensaje informativo
        })


class ReporteEutanasiasView(LoginRequiredMixin, View):
    template_name = 'reportes/reporte_eutanasias.html'
    
    def get(self, request):
        # Obtener fechas del formulario
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')
        
        # Calcular fechas por defecto (mes actual)
        hoy = timezone.now().date()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Usar fechas del formulario o fechas por defecto
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            except ValueError:
                # Si hay error en las fechas, usar fechas por defecto
                fecha_inicio = primer_dia_mes
                fecha_fin = ultimo_dia_mes
        else:
            # Si no hay fechas en el formulario, usar fechas por defecto
            fecha_inicio = primer_dia_mes
            fecha_fin = ultimo_dia_mes
        
        # Obtener eutanasias en el rango de fechas (siempre se ejecuta)
        eutanasias = Consulta.objects.filter(
            es_eutanasia=True,
            cita__fecha__date__gte=fecha_inicio,
            cita__fecha__date__lte=fecha_fin
        ).select_related('cita__mascota__cliente', 'cita__mascota__especie').order_by('-cita__fecha')
        
        # Estadísticas por especie
        stats_especies = Consulta.objects.filter(
            es_eutanasia=True,
            cita__fecha__date__gte=fecha_inicio,
            cita__fecha__date__lte=fecha_fin
        ).values('cita__mascota__especie__nombre').annotate(total=Count('id')).order_by('-total')
        
        return render(request, self.template_name, {
            'eutanasias': eutanasias,
            'stats_especies': stats_especies,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_eutanasias': eutanasias.count(),
            'es_filtro_defecto': not (fecha_inicio_str and fecha_fin_str),  # Para mostrar un mensaje informativo
        })