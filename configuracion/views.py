from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Especie, Raza
from .forms import EspecieForm, RazaForm

@login_required
def lista_especies(request):
    especies = Especie.objects.all().order_by('nombre')
    return render(request, 'configuracion/lista_especies.html', {
        'especies': especies
    })

@login_required
def crear_especie(request):
    if request.method == 'POST':
        form = EspecieForm(request.POST)
        if form.is_valid():
            especie = form.save()
            messages.success(request, f"Especie {especie.nombre} creada correctamente")
            return redirect('lista_especies')
    else:
        form = EspecieForm()
    return render(request, 'configuracion/crear_especie.html', {'form': form})

@login_required
def editar_especie(request, pk):
    especie = get_object_or_404(Especie, pk=pk)
    if request.method == 'POST':
        form = EspecieForm(request.POST, instance=especie)
        if form.is_valid():
            especie = form.save()
            messages.success(request, f"Especie {especie.nombre} actualizada correctamente")
            return redirect('lista_especies')
    else:
        form = EspecieForm(instance=especie)
    return render(request, 'configuracion/editar_especie.html', {
        'form': form,
        'especie': especie
    })

@login_required
def eliminar_especie(request, pk):
    especie = get_object_or_404(Especie, pk=pk)
    if request.method == 'POST':
        nombre = especie.nombre
        try:
            especie.delete()
            messages.success(request, f"Especie {nombre} eliminada correctamente")
        except Exception as e:
            messages.error(request, f"No se puede eliminar la especie porque tiene razas asociadas" )
        return redirect('lista_especies')
    return render(request, 'configuracion/eliminar_especie.html', {
        'especie': especie
    })

@login_required
def lista_razas(request):
    especie_id = request.GET.get('especie_id')
    razas = Raza.objects.all()
    
    if especie_id:
        razas = razas.filter(especie_id=especie_id)
    
    razas = razas.order_by('especie__nombre', 'nombre')
    
    especies = Especie.objects.all().order_by('nombre')
    
    return render(request, 'configuracion/lista_razas.html', {
        'razas': razas,
        'especies': especies,
        'especie_id': especie_id
    })

@login_required
def crear_raza(request):
    if request.method == 'POST':
        form = RazaForm(request.POST)
        if form.is_valid():
            raza = form.save()
            messages.success(request, f"Raza {raza.nombre} creada correctamente")
            return redirect('lista_razas')
    else:
        form = RazaForm()
    return render(request, 'configuracion/crear_raza.html', {'form': form})

@login_required
def editar_raza(request, pk):
    raza = get_object_or_404(Raza, pk=pk)
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if form.is_valid():
            raza = form.save()
            messages.success(request, f"Raza {raza.nombre} actualizada correctamente")
            return redirect('lista_razas')
    else:
        form = RazaForm(instance=raza)
    return render(request, 'configuracion/editar_raza.html', {
        'form': form,
        'raza': raza
    })

@login_required
def eliminar_raza(request, pk):
    raza = get_object_or_404(Raza, pk=pk)
    if request.method == 'POST':
        nombre = raza.nombre
        raza.delete()
        messages.success(request, f"Raza {nombre} eliminada correctamente")
        return redirect('lista_razas')
    return render(request, 'configuracion/eliminar_raza.html', {
        'raza': raza
    })