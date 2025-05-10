from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from consultas.models import Cita, Consulta
from inventario.models import VacunaAplicada, ProductoAplicado
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
import calendar

@login_required
def dashboard(request):
    # Citas para hoy
    hoy = timezone.now().date()
    citas_hoy = Cita.objects.filter(fecha__date=hoy, atendida=False).order_by('fecha')
    
    # Citas próximas (próximos 7 días, excluyendo hoy)
    manana = hoy + timedelta(days=1)
    en_una_semana = hoy + timedelta(days=7)
    citas_proximas = Cita.objects.filter(
        fecha__date__gte=manana,
        fecha__date__lte=en_una_semana,
        atendida=False
    ).order_by('fecha')
    
    # Próximas vacunas a aplicar (en los próximos 14 días)
    proximas_vacunas = VacunaAplicada.objects.filter(
        fecha_proxima__gte=hoy,
        fecha_proxima__lte=hoy + timedelta(days=14)
    ).order_by('fecha_proxima')
    
    # Próximos productos a aplicar (en los próximos 14 días)
    proximos_productos = ProductoAplicado.objects.filter(
        fecha_proxima__gte=hoy,
        fecha_proxima__lte=hoy + timedelta(days=14)
    ).order_by('fecha_proxima')
    
    context = {
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas,
        'proximas_vacunas': proximas_vacunas,
        'proximos_productos': proximos_productos,
    }
    
    return render(request, 'reportes/dashboard.html', context)

@login_required
def reporte_citas(request):
    # Obtener parámetros de filtrado
    fecha_inicio_str = request.GET.get('fecha_inicio', '')
    fecha_fin_str = request.GET.get('fecha_fin', '')
    atendida = request.GET.get('atendida', '')
    
    # Fechas por defecto si no se especifican
    if not fecha_inicio_str:
        fecha_inicio = timezone.now().date() - timedelta(days=30)
    else:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    
    if not fecha_fin_str:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    
    # Filtrar citas
    citas = Cita.objects.filter(fecha__date__gte=fecha_inicio, fecha__date__lte=fecha_fin)
    
    if atendida == 'si':
        citas = citas.filter(atendida=True)
    elif atendida == 'no':
        citas = citas.filter(atendida=False)
    
    citas = citas.order_by('-fecha')
    
    return render(request, 'reportes/reporte_citas.html', {
        'citas': citas,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
        'atendida': atendida,
    })

@login_required
def reporte_vacunas(request):
    # Obtener parámetros de filtrado
    fecha_inicio_str = request.GET.get('fecha_inicio', '')
    fecha_fin_str = request.GET.get('fecha_fin', '')
    vacuna_id = request.GET.get('vacuna_id', '')
    
    # Fechas por defecto si no se especifican
    if not fecha_inicio_str:
        fecha_inicio = timezone.now().date() - timedelta(days=90)
    else:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    
    if not fecha_fin_str:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    
    # Filtrar vacunas aplicadas
    vacunas_aplicadas = VacunaAplicada.objects.filter(
        fecha_aplicacion__gte=fecha_inicio, 
        fecha_aplicacion__lte=fecha_fin
    )
    
    if vacuna_id:
        vacunas_aplicadas = vacunas_aplicadas.filter(vacuna_id=vacuna_id)
    
    vacunas_aplicadas = vacunas_aplicadas.order_by('-fecha_aplicacion')
    
    # Obtener lista de vacunas para el selector de filtrado
    from inventario.models import Vacuna
    vacunas = Vacuna.objects.all().order_by('nombre')
    
    return render(request, 'reportes/reporte_vacunas.html', {
        'vacunas_aplicadas': vacunas_aplicadas,
        'vacunas': vacunas,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
        'vacuna_id': vacuna_id,
    })

@login_required
def reporte_productos(request):
    # Obtener parámetros de filtrado
    fecha_inicio_str = request.GET.get('fecha_inicio', '')
    fecha_fin_str = request.GET.get('fecha_fin', '')
    producto_id = request.GET.get('producto_id', '')
    tipo = request.GET.get('tipo', '')
    
    # Fechas por defecto si no se especifican
    if not fecha_inicio_str:
        fecha_inicio = timezone.now().date() - timedelta(days=90)
    else:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    
    if not fecha_fin_str:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    
    # Filtrar productos aplicados
    productos_aplicados = ProductoAplicado.objects.filter(
        fecha_aplicacion__gte=fecha_inicio, 
        fecha_aplicacion__lte=fecha_fin
    )
    
    if producto_id:
        productos_aplicados = productos_aplicados.filter(producto_id=producto_id)
    
    if tipo:
        productos_aplicados = productos_aplicados.filter(producto__tipo=tipo)
    
    productos_aplicados = productos_aplicados.order_by('-fecha_aplicacion')
    
    # Obtener lista de productos para el selector de filtrado
    from inventario.models import Producto
    productos = Producto.objects.all().order_by('nombre')
    
    return render(request, 'reportes/reporte_productos.html', {
        'productos_aplicados': productos_aplicados,
        'productos': productos,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
        'producto_id': producto_id,
        'tipo': tipo,
    })

@login_required
def reporte_eutanasias(request):
    # Obtener parámetros de filtrado
    fecha_inicio_str = request.GET.get('fecha_inicio', '')
    fecha_fin_str = request.GET.get('fecha_fin', '')
    
    # Fechas por defecto si no se especifican
    if not fecha_inicio_str:
        fecha_inicio = timezone.now().date() - timedelta(days=365)
    else:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
    
    if not fecha_fin_str:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    
    # Filtrar consultas de eutanasia
    eutanasias = Consulta.objects.filter(
        es_eutanasia=True,
        fecha_registro__date__gte=fecha_inicio,
        fecha_registro__date__lte=fecha_fin
    ).order_by('-fecha_registro')
    
    return render(request, 'reportes/reporte_eutanasias.html', {
        'eutanasias': eutanasias,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
    })
    
#------------------------------------------------ BLOQUE A DISCUTIR -----------------------------------------
@login_required
def dashboard_view(request):
    # Obtener estadísticas para el dashboard
    hoy = datetime.now().date()
    citas_hoy = Cita.objects.filter(fecha__date=hoy).count()
    citas_pendientes = Cita.objects.filter(fecha__date__gt=hoy, programada=True).count()
    vacunas_mes = VacunaAplicada.objects.filter(fecha_aplicacion__month=hoy.month, fecha_aplicacion__year=hoy.year).count()
    
    # Obtener recordatorios para vacunas y productos
    recordatorios_vacunas = VacunaAplicada.objects.filter(
        fecha_proxima__range=[hoy, hoy + timedelta(days=15)]
    ).select_related('mascota', 'mascota__cliente', 'vacuna')
    
    recordatorios_productos = ProductoAplicado.objects.filter(
        fecha_proxima__range=[hoy, hoy + timedelta(days=15)]
    ).select_related('mascota', 'mascota__cliente', 'producto')
    
    return render(request, 'dashboard.html', {
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'vacunas_mes': vacunas_mes,
        'recordatorios_vacunas': recordatorios_vacunas,
        'recordatorios_productos': recordatorios_productos,
    })

class ReporteCitasView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/reporte_citas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener fechas desde parámetros o usar valores predeterminados
        fecha_inicio_str = self.request.GET.get('fecha_inicio')
        fecha_fin_str = self.request.GET.get('fecha_fin')
        
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else (datetime.now().date() - timedelta(days=30))
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else datetime.now().date()
        except ValueError:
            fecha_inicio = datetime.now().date() - timedelta(days=30)
            fecha_fin = datetime.now().date()
        
        # Obtener citas en el rango de fechas
        citas = Cita.objects.filter(
            fecha__date__range=[fecha_inicio, fecha_fin]
        ).select_related('mascota', 'mascota__cliente')
        
        # Agrupar por día
        citas_por_dia = citas.annotate(
            dia=TruncMonth('fecha')
        ).values('dia').annotate(total=Count('id')).order_by('dia')
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        context['citas'] = citas
        context['citas_por_dia'] = citas_por_dia
        return context

class ReporteVacunasView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/reporte_vacunas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener fechas desde parámetros o usar valores predeterminados
        fecha_inicio_str = self.request.GET.get('fecha_inicio')
        fecha_fin_str = self.request.GET.get('fecha_fin')
        
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else (datetime.now().date() - timedelta(days=30))
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else datetime.now().date()
        except ValueError:
            fecha_inicio = datetime.now().date() - timedelta(days=30)
            fecha_fin = datetime.now().date()
        
        # Obtener vacunas aplicadas en el rango de fechas
        vacunas = VacunaAplicada.objects.filter(
            fecha_aplicacion__range=[fecha_inicio, fecha_fin]
        ).select_related('mascota', 'mascota__cliente', 'vacuna')
        
        # Agrupar por vacuna
        vacunas_por_tipo = vacunas.values(
            'vacuna__nombre'
        ).annotate(total=Count('id')).order_by('-total')
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        context['vacunas'] = vacunas
        context['vacunas_por_tipo'] = vacunas_por_tipo
        return context

class ReporteProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/reporte_productos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener fechas desde parámetros o usar valores predeterminados
        fecha_inicio_str = self.request.GET.get('fecha_inicio')
        fecha_fin_str = self.request.GET.get('fecha_fin')
        
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else (datetime.now().date() - timedelta(days=30))
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else datetime.now().date()
        except ValueError:
            fecha_inicio = datetime.now().date() - timedelta(days=30)
            fecha_fin = datetime.now().date()
        
        # Obtener productos aplicados en el rango de fechas
        productos = ProductoAplicado.objects.filter(
            fecha_aplicacion__range=[fecha_inicio, fecha_fin]
        ).select_related('mascota', 'mascota__cliente', 'producto')
        
        # Agrupar por producto
        productos_por_tipo = productos.values(
            'producto__nombre', 'producto__tipo'
        ).annotate(total=Count('id')).order_by('-total')
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        context['productos'] = productos
        context['productos_por_tipo'] = productos_por_tipo
        return context

class ReporteEutanasiasView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/reporte_eutanasias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener fechas desde parámetros o usar valores predeterminados
        fecha_inicio_str = self.request.GET.get('fecha_inicio')
        fecha_fin_str = self.request.GET.get('fecha_fin')
        
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else (datetime.now().date() - timedelta(days=365))
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else datetime.now().date()
        except ValueError:
            fecha_inicio = datetime.now().date() - timedelta(days=365)
            fecha_fin = datetime.now().date()
        
        # Obtener eutanasias en el rango de fechas
        eutanasias = Consulta.objects.filter(
            es_eutanasia=True,
            fecha_consulta__date__range=[fecha_inicio, fecha_fin]
        ).select_related('cita', 'cita__mascota', 'cita__mascota__cliente', 'cita__mascota__especie')
        
        # Agrupar por especie
        eutanasias_por_especie = eutanasias.values(
            'cita__mascota__especie__nombre'
        ).annotate(total=Count('id')).order_by('-total')
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        context['eutanasias'] = eutanasias
        context['eutanasias_por_especie'] = eutanasias_por_especie
        return context