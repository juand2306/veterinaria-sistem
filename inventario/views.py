from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from clientes.models import Mascota
from .models import Vacuna, VacunaAplicada, Producto, ProductoAplicado
from .forms import VacunaForm, VacunaAplicadaForm, ProductoForm, ProductoAplicadoForm

# Vistas para Vacunas
class VacunaListView(LoginRequiredMixin, ListView):
    model = Vacuna
    template_name = 'inventario/lista_vacunas.html'
    context_object_name = 'vacunas'
    ordering = ['nombre']


class VacunaDetailView(LoginRequiredMixin, DetailView):
    model = Vacuna
    template_name = 'inventario/detalle_vacuna.html'
    context_object_name = 'vacuna'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Listar todas las aplicaciones de esta vacuna
        context['aplicaciones'] = VacunaAplicada.objects.filter(vacuna=self.object).order_by('-fecha_aplicacion')
        return context


class VacunaCreateView(LoginRequiredMixin, CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'inventario/vacuna_form.html'
    success_url = reverse_lazy('inventario:lista_vacunas')
    
    def form_valid(self, form):
        messages.success(self.request, "Vacuna creada exitosamente.")
        return super().form_valid(form)


class VacunaUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'inventario/vacuna_form.html'
    
    def get_success_url(self):
        return reverse_lazy('inventario:detalle_vacuna', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, "Vacuna actualizada exitosamente.")
        return super().form_valid(form)


class VacunaDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacuna
    template_name = 'inventario/confirmar_eliminar_vacuna.html'
    success_url = reverse_lazy('inventario:lista_vacunas')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Vacuna eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Vacunas Aplicadas
class VacunaAplicadaCreateView(LoginRequiredMixin, CreateView):
    model = VacunaAplicada
    form_class = VacunaAplicadaForm
    template_name = 'inventario/vacuna_aplicada_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasamos la mascota al formulario
        mascota_id = self.kwargs.get('mascota_id')
        kwargs['mascota_id'] = mascota_id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mascota_id = self.kwargs.get('mascota_id')
        context['mascota'] = get_object_or_404(Mascota, pk=mascota_id)
        return context
    
    def form_valid(self, form):
        mascota_id = self.kwargs.get('mascota_id')
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        form.instance.mascota = mascota
        
        messages.success(self.request, "Vacuna aplicada exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': self.kwargs.get('mascota_id')})


class VacunaAplicadaDetailView(LoginRequiredMixin, DetailView):
    model = VacunaAplicada
    template_name = 'inventario/detalle_vacuna_aplicada.html'
    context_object_name = 'vacuna_aplicada'


class VacunaAplicadaUpdateView(LoginRequiredMixin, UpdateView):
    model = VacunaAplicada
    form_class = VacunaAplicadaForm
    template_name = 'inventario/vacuna_aplicada_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['mascota_id'] = self.object.mascota.id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascota'] = self.object.mascota
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Registro de vacuna actualizado exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': self.object.mascota.id})


class VacunaAplicadaDeleteView(LoginRequiredMixin, DeleteView):
    model = VacunaAplicada
    template_name = 'inventario/confirmar_eliminar_vacuna_aplicada.html'
    
    def get_success_url(self):
        mascota_id = self.object.mascota.id
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': mascota_id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Registro de vacuna eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Productos (Antiparasitarios/Vermífugos)
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/lista_productos.html'
    context_object_name = 'productos'
    ordering = ['nombre']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por tipo si se proporciona
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'inventario/detalle_producto.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Listar todas las aplicaciones de este producto
        context['aplicaciones'] = ProductoAplicado.objects.filter(producto=self.object).order_by('-fecha_aplicacion')
        return context


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('inventario:lista_productos')
    
    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    
    def get_success_url(self):
        return reverse_lazy('inventario:detalle_producto', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/confirmar_eliminar_producto.html'
    success_url = reverse_lazy('inventario:lista_productos')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Productos Aplicados
class ProductoAplicadoCreateView(LoginRequiredMixin, CreateView):
    model = ProductoAplicado
    form_class = ProductoAplicadoForm
    template_name = 'inventario/producto_aplicado_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasamos la mascota al formulario
        mascota_id = self.kwargs.get('mascota_id')
        kwargs['mascota_id'] = mascota_id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mascota_id = self.kwargs.get('mascota_id')
        context['mascota'] = get_object_or_404(Mascota, pk=mascota_id)
        return context
    
    def form_valid(self, form):
        mascota_id = self.kwargs.get('mascota_id')
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        form.instance.mascota = mascota
        
        messages.success(self.request, "Producto aplicado exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': self.kwargs.get('mascota_id')})


class ProductoAplicadoDetailView(LoginRequiredMixin, DetailView):
    model = ProductoAplicado
    template_name = 'inventario/detalle_producto_aplicado.html'
    context_object_name = 'producto_aplicado'


class ProductoAplicadoUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductoAplicado
    form_class = ProductoAplicadoForm
    template_name = 'inventario/producto_aplicado_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['mascota_id'] = self.object.mascota.id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mascota'] = self.object.mascota
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Registro de producto actualizado exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': self.object.mascota.id})


class ProductoAplicadoDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductoAplicado
    template_name = 'inventario/confirmar_eliminar_producto_aplicado.html'
    
    def get_success_url(self):
        mascota_id = self.object.mascota.id
        return reverse_lazy('clientes:detalle_mascota', kwargs={'pk': mascota_id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Registro de producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
    
    
    
@login_required
def dashboard_inventario(request):
    """Vista para el dashboard de inventario que muestra resúmenes y estadísticas."""
    
    # Fecha actual para comparaciones
    hoy = timezone.now().date()
    
    # Próximos 30 días para alertas
    fecha_limite = hoy + timedelta(days=30)
    
    # Contadores básicos
    total_vacunas = Vacuna.objects.count()
    total_productos = Producto.objects.count()
    
    # Próximas vacunaciones (con fecha_proxima en los próximos 30 días o vencidas)
    proximas_vacunas = VacunaAplicada.objects.filter(
        fecha_proxima__lte=fecha_limite
    ).select_related('mascota', 'vacuna').order_by('fecha_proxima')
    
    # Agregar días restantes a cada vacuna
    for vacuna in proximas_vacunas:
        if vacuna.fecha_proxima:
            delta = vacuna.fecha_proxima - hoy
            vacuna.dias_restantes = delta.days
        else:
            vacuna.dias_restantes = None
    
    # Próximas aplicaciones de productos
    proximos_productos = ProductoAplicado.objects.filter(
        fecha_proxima__lte=fecha_limite
    ).select_related('mascota', 'producto').order_by('fecha_proxima')
    
    # Agregar días restantes a cada producto
    for producto in proximos_productos:
        if producto.fecha_proxima:
            delta = producto.fecha_proxima - hoy
            producto.dias_restantes = delta.days
        else:
            producto.dias_restantes = None
    
    # Estadísticas: Vacunas más aplicadas
    vacunas_aplicadas = VacunaAplicada.objects.values(
        'vacuna__nombre', 'vacuna_id'
    ).annotate(count=Count('id')).order_by('-count')[:5]
    
    # Calcular porcentajes para las vacunas más aplicadas
    total_aplicaciones_vacunas = sum(item['count'] for item in vacunas_aplicadas)
    vacunas_populares = []
    
    if total_aplicaciones_vacunas > 0:
        for item in vacunas_aplicadas:
            porcentaje = (item['count'] / total_aplicaciones_vacunas) * 100
            vacunas_populares.append({
                'nombre': item['vacuna__nombre'],
                'count': item['count'],
                'porcentaje': porcentaje
            })
    
    # Estadísticas: Productos más aplicados
    productos_aplicados = ProductoAplicado.objects.values(
        'producto__nombre', 'producto__tipo', 'producto_id'
    ).annotate(count=Count('id')).order_by('-count')[:5]
    
    # Calcular porcentajes para los productos más aplicados
    total_aplicaciones_productos = sum(item['count'] for item in productos_aplicados)
    productos_populares = []
    
    if total_aplicaciones_productos > 0:
        for item in productos_aplicados:
            porcentaje = (item['count'] / total_aplicaciones_productos) * 100
            productos_populares.append({
                'nombre': item['producto__nombre'],
                'tipo': item['producto__tipo'],
                'count': item['count'],
                'porcentaje': porcentaje,
                'get_tipo_display': 'Vermífugo' if item['producto__tipo'] == 'V' else 'Antiparasitario'
            })
    
    context = {
        'total_vacunas': total_vacunas,
        'total_productos': total_productos,
        'proximas_vacunaciones': proximas_vacunas.count(),
        'proximas_aplicaciones': proximos_productos.count(),
        'proximas_vacunas': proximas_vacunas,
        'proximos_productos': proximos_productos,
        'vacunas_populares': vacunas_populares,
        'productos_populares': productos_populares,
        'hoy': hoy.strftime('%Y-%m-%d')
    }
    
    return render(request, 'inventario/dashboard_inventario.html', context)