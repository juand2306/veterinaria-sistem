from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Cliente, Mascota, ImagenDiagnostica
from .forms import ClienteForm, MascotaForm, ImagenDiagnosticaForm
from configuracion.models import Raza

@login_required
def lista_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all()
    
    if query:
        clientes = clientes.filter(nombre__icontains=query)
    
    paginator = Paginator(clientes, 10)  # 10 clientes por página
    page = request.GET.get('page')
    clientes_paginados = paginator.get_page(page)
    
    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes_paginados,
        'query': query
    })

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f"Cliente {cliente.nombre} creado correctamente")
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f"Cliente {cliente.nombre} actualizado correctamente")
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/editar_cliente.html', {
        'form': form,
        'cliente': cliente
    })

@login_required
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    mascotas = cliente.mascotas.all()
    
    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'mascotas': mascotas
    })

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        nombre = cliente.nombre
        cliente.delete()
        messages.success(request, f"Cliente {nombre} eliminado correctamente")
        return redirect('lista_clientes')
    
    return render(request, 'clientes/eliminar_cliente.html', {
        'cliente': cliente
    })

@login_required
def crear_mascota(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.cliente = cliente
            mascota.save()
            messages.success(request, f"Mascota {mascota.nombre} creada correctamente")
            return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = MascotaForm()
    
    return render(request, 'clientes/crear_mascota.html', {
        'form': form,
        'cliente': cliente
    })

@login_required
def detalle_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    imagenes = mascota.imagenes.all()
    vacunas = mascota.vacunas_aplicadas.all().order_by('-fecha_aplicacion')
    productos = mascota.productos_aplicados.all().order_by('-fecha_aplicacion')
    citas = mascota.citas.all().order_by('-fecha')
    
    return render(request, 'clientes/detalle_mascota.html', {
        'mascota': mascota,
        'imagenes': imagenes,
        'vacunas': vacunas,
        'productos': productos,
        'citas': citas
    })

@login_required
def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            mascota = form.save()
            messages.success(request, f"Mascota {mascota.nombre} actualizada correctamente")
            return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'clientes/editar_mascota.html', {
        'form': form,
        'mascota': mascota
    })

@login_required
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    
    if request.method == 'POST':
        cliente_id = mascota.cliente.id
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f"Mascota {nombre} eliminada correctamente")
        return redirect('detalle_cliente', pk=cliente_id)
    
    return render(request, 'clientes/eliminar_mascota.html', {
        'mascota': mascota
    })

@login_required
def cargar_razas(request):
    especie_id = request.GET.get('especie_id')
    razas = Raza.objects.filter(especie_id=especie_id).order_by('nombre')
    return JsonResponse(list(razas.values('id', 'nombre')), safe=False)

@login_required
def agregar_imagen(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    
    if request.method == 'POST':
        form = ImagenDiagnosticaForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.mascota = mascota
            imagen.save()
            messages.success(request, "Imagen diagnóstica agregada correctamente")
            return redirect('detalle_mascota', pk=mascota.pk)
    else:
        form = ImagenDiagnosticaForm()
    
    return render(request, 'clientes/agregar_imagen.html', {
        'form': form,
        'mascota': mascota
    })