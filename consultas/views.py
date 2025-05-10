from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Cita, Consulta
from .forms import CitaForm, ConsultaForm
from clientes.models import Mascota

@login_required
def lista_citas(request):
    estado = request.GET.get('estado', 'pendientes')
    fecha_inicio = request.GET.get('fecha_inicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.GET.get('fecha_fin', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
    
    citas = Cita.objects.all()
    
    # Filtrado por estado
    if estado == 'pendientes':
        citas = citas.filter(atendida=False, fecha__gte=datetime.now())
    elif estado == 'atendidas':
        citas = citas.filter(atendida=True)
    elif estado == 'todas':
        pass  # No se aplica filtro adicional
    
    # Filtro por rango de fechas
    if fecha_inicio:
        citas = citas.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        citas = citas.filter(fecha__lte=fecha_fin)
    
    # Ordenar por fecha
    citas = citas.order_by('fecha')
    
    paginator = Paginator(citas, 10)  # 10 citas por página
    page = request.GET.get('page')
    citas_paginadas = paginator.get_page(page)
    
    return render(request, 'consultas/lista_citas.html', {
        'citas': citas_paginadas,
        'estado': estado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

@login_required
def crear_cita(request, mascota_id=None):
    mascota_inicial = None
    if mascota_id:
        mascota_inicial = get_object_or_404(Mascota, pk=mascota_id)
        # Verificar que la mascota esté activa
        if not mascota_inicial.activa:
            messages.error(request, "No se pueden agendar citas para mascotas inactivas")
            return redirect('detalle_mascota', pk=mascota_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            mascota = form.cleaned_data['mascota']
            if not mascota.activa:
                messages.error(request, "No se pueden agendar citas para mascotas inactivas")
                return redirect('detalle_mascota', pk=mascota.id)
            
            cita = form.save()
            messages.success(request, f"Cita para {cita.mascota.nombre} agendada correctamente")
            
            # Redireccionar a la mascota o a la lista de citas
            if 'siguiente' in request.POST and request.POST['siguiente'] == 'mascota':
                return redirect('detalle_mascota', pk=cita.mascota.id)
            else:
                return redirect('lista_citas')
    else:
        initial_data = {}
        if mascota_inicial:
            initial_data['mascota'] = mascota_inicial
        
        form = CitaForm(initial=initial_data)
    
    context = {'form': form}
    if mascota_inicial:
        context['mascota'] = mascota_inicial
    
    return render(request, 'consultas/crear_cita.html', context)

@login_required
def detalle_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    consulta = None
    
    try:
        consulta = cita.consulta
    except Consulta.DoesNotExist:
        pass
    
    return render(request, 'consultas/detalle_cita.html', {
        'cita': cita,
        'consulta': consulta
    })

@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    # No permitir editar citas ya atendidas
    if cita.atendida:
        messages.error(request, "No se puede editar una cita que ya ha sido atendida")
        return redirect('detalle_cita', pk=cita.pk)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save()
            messages.success(request, f"Cita para {cita.mascota.nombre} actualizada correctamente")
            return redirect('detalle_cita', pk=cita.pk)
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'consultas/editar_cita.html', {
        'form': form,
        'cita': cita
    })

@login_required
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    
    # No permitir eliminar citas ya atendidas
    if cita.atendida:
        messages.error(request, "No se puede eliminar una cita que ya ha sido atendida")
        return redirect('detalle_cita', pk=cita.pk)
    
    if request.method == 'POST':
        mascota_id = cita.mascota.id
        cita.delete()
        messages.success(request, "Cita eliminada correctamente")
        
        # Redireccionar a la mascota o a la lista de citas
        if 'siguiente' in request.POST and request.POST['siguiente'] == 'mascota':
            return redirect('detalle_mascota', pk=mascota_id)
        else:
            return redirect('lista_citas')
    
    return render(request, 'consultas/eliminar_cita.html', {
        'cita': cita
    })

@login_required
def registrar_consulta(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    
    # Verificar si ya tiene una consulta registrada
    try:
        consulta = cita.consulta
        messages.error(request, "Esta cita ya tiene una consulta registrada")
        return redirect('detalle_cita', pk=cita.pk)
    except Consulta.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.cita = cita
            
            # Si es eutanasia, marcar mascota como inactiva automáticamente
            # (esto se maneja en el save() del modelo Consulta)
            consulta.save()
            
            messages.success(request, "Consulta registrada correctamente")
            
            # Redireccionar según lo solicitado
            if 'siguiente' in request.POST and request.POST['siguiente'] == 'mascota':
                return redirect('detalle_mascota', pk=cita.mascota.id)
            else:
                return redirect('detalle_cita', pk=cita.pk)
    else:
        form = ConsultaForm()
    
    return render(request, 'consultas/registrar_consulta.html', {
        'form': form,
        'cita': cita
    })

@login_required
def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    cita = consulta.cita
    
    # Guardar el estado previo de es_eutanasia
    es_eutanasia_previo = consulta.es_eutanasia
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            # Si cambia de no-eutanasia a eutanasia, se manejará en el save() del modelo
            # Si cambia de eutanasia a no-eutanasia, necesitamos gestionar la mascota manualmente
            if es_eutanasia_previo and not form.cleaned_data['es_eutanasia']:
                # Advertir que la mascota seguirá inactiva
                messages.warning(request, 
                    "Se ha cambiado la consulta de eutanasia a no-eutanasia, pero la mascota seguirá marcada como inactiva. " +
                    "Debe activarla manualmente si es necesario.")
            
            consulta = form.save()
            messages.success(request, "Consulta actualizada correctamente")
            return redirect('detalle_cita', pk=cita.pk)
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'consultas/editar_consulta.html', {
        'form': form,
        'consulta': consulta,
        'cita': cita
    })