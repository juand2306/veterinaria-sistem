from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from clientes.models import Mascota
from .models import Cita, Consulta
from .forms import CitaForm, ConsultaForm

# Vistas para Citas
class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'consultas/lista_citas.html'
    context_object_name = 'citas'
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por fecha si se proporciona en la URL
        fecha_filtro = self.request.GET.get('fecha')
        if fecha_filtro:
            queryset = queryset.filter(fecha__date=fecha_filtro)
        return queryset


class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'consultas/detalle_cita.html'
    context_object_name = 'cita'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comprobar si hay una consulta asociada a esta cita
        consulta = Consulta.objects.filter(cita=self.object).first()
        context['consulta'] = consulta
        return context


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'consultas/cita_form.html'
    success_url = reverse_lazy('consultas:lista_citas')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Si se proporciona un id de mascota en la URL, lo pasamos al formulario
        mascota_id = self.kwargs.get('mascota_id')
        if mascota_id:
            kwargs['mascota_id'] = mascota_id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mascota_id = self.kwargs.get('mascota_id')
        if mascota_id:
            context['mascota'] = get_object_or_404(Mascota, pk=mascota_id)
        return context
    
    def form_valid(self, form):
        mascota_id = self.kwargs.get('mascota_id')
        if mascota_id:
            mascota = get_object_or_404(Mascota, pk=mascota_id)
            form.instance.mascota = mascota
        
        messages.success(self.request, "Cita creada exitosamente.")
        return super().form_valid(form)


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'consultas/cita_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasamos el id de la mascota al formulario
        kwargs['mascota_id'] = self.object.mascota.id
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('consultas:detalle_cita', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, "Cita actualizada exitosamente.")
        return super().form_valid(form)


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'consultas/confirmar_eliminar_cita.html'
    success_url = reverse_lazy('consultas:lista_citas')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cita eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Consultas
class ConsultaCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consultas/consulta_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasamos la cita al formulario
        kwargs['cita_id'] = self.kwargs.get('cita_id')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cita_id = self.kwargs.get('cita_id')
        cita = get_object_or_404(Cita, pk=cita_id)
        context['cita'] = cita
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        cita_id = self.kwargs.get('cita_id')
        cita = get_object_or_404(Cita, pk=cita_id)
        form.instance.cita = cita
        
        # Si la consulta es una eutanasia, marcar la mascota como inactiva
        if form.cleaned_data.get('es_eutanasia'):
            mascota = cita.mascota
            mascota.activa = False
            mascota.save()
        
        messages.success(self.request, "Consulta registrada exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('consultas:detalle_cita', kwargs={'pk': self.kwargs.get('cita_id')})


class ConsultaDetailView(LoginRequiredMixin, DetailView):
    model = Consulta
    template_name = 'consultas/detalle_consulta.html'
    context_object_name = 'consulta'


class ConsultaUpdateView(LoginRequiredMixin, UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consultas/consulta_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cita_id'] = self.object.cita.id
        return kwargs
    
    @transaction.atomic
    def form_valid(self, form):
        # Verificar si cambió el estado de eutanasia
        consulta = self.get_object()
        mascota = consulta.cita.mascota
        
        # Si ahora es eutanasia y antes no lo era
        if form.cleaned_data.get('es_eutanasia') and not consulta.es_eutanasia:
            mascota.activa = False
            mascota.save()
        # Si ahora NO es eutanasia pero antes lo era
        elif not form.cleaned_data.get('es_eutanasia') and consulta.es_eutanasia:
            mascota.activa = True
            mascota.save()
        
        messages.success(self.request, "Consulta actualizada exitosamente.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('consultas:detalle_consulta', kwargs={'pk': self.object.pk})


class ConsultaDeleteView(LoginRequiredMixin, DeleteView):
    model = Consulta
    template_name = 'consultas/confirmar_eliminar_consulta.html'
    
    def get_success_url(self):
        cita_id = self.object.cita.id
        return reverse_lazy('consultas:detalle_cita', kwargs={'pk': cita_id})
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        consulta = self.get_object()
        cita = consulta.cita
        
        # Si era una eutanasia, reactivar la mascota
        if consulta.es_eutanasia:
            mascota = cita.mascota
            mascota.activa = True
            mascota.save()
        
        messages.success(self.request, "Consulta eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vista para la historia clínica - Esta vista combina datos de varias tablas
class HistoriaClinicaView(LoginRequiredMixin, View):
    template_name = 'consultas/historia_clinica.html'
    
    def get(self, request, mascota_id):
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        consultas = Consulta.objects.filter(cita__mascota=mascota).order_by('-cita__fecha')
        
        # Podemos obtener vacunas y productos aplicados si hemos definido esos modelos
        vacunas_aplicadas = []  # VacunaAplicada.objects.filter(mascota=mascota)
        productos_aplicados = []  # ProductoAplicado.objects.filter(mascota=mascota)
        
        context = {
            'mascota': mascota,
            'consultas': consultas,
            'vacunas_aplicadas': vacunas_aplicadas,
            'productos_aplicados': productos_aplicados,
        }
        return render(request, self.template_name, context)