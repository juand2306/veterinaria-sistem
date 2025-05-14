from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

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