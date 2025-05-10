from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Vacuna, VacunaAplicada, Producto, ProductoAplicado
from .forms import VacunaForm, VacunaAplicadaForm, ProductoForm, ProductoAplicadoForm
from clientes.models import Mascota
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# ----- VACUNAS -----
@login_required
def lista_vacunas(request):
    vacunas = Vacuna.objects.all().order_by('nombre')
    
    return render(request, 'inventario/lista_vacunas.html', {
        'vacunas': vacunas
    })

@login_required
def crear_vacuna(request):
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save()
            messages.success(request, f"Vacuna {vacuna.nombre} creada correctamente")
            return redirect('lista_vacunas')
    else:
        form = VacunaForm()
    
    return render(request, 'inventario/crear_vacuna.html', {'form': form})

@login_required
def editar_vacuna(request, pk):
    vacuna = get_object_or_404(Vacuna, pk=pk)
    
    if request.method == 'POST':
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            vacuna = form.save()
            messages.success(request, f"Vacuna {vacuna.nombre} actualizada correctamente")
            return redirect('lista_vacunas')
    else:
        form = VacunaForm(instance=vacuna)
    
    return render(request, 'inventario/editar_vacuna.html', {
        'form': form,
        'vacuna': vacuna
    })

@login_required
def eliminar_vacuna(request, pk):
    vacuna = get_object_or_404(Vacuna, pk=pk)
    
    if request.method == 'POST':
        nombre = vacuna.nombre
        vacuna.delete()
        messages.success(request, f"Vacuna {nombre} eliminada correctamente")
        return redirect('lista_vacunas')
    
    return render(request, 'inventario/eliminar_vacuna.html', {
        'vacuna': vacuna
    })

# ----- VACUNAS APLICADAS -----
@login_required
def aplicar_vacuna(request, mascota_id=None):
    mascota_inicial = None
    if mascota_id:
        mascota_inicial = get_object_or_404(Mascota, pk=mascota_id)
        # Verificar que la mascota esté activa
        if not mascota_inicial.activa:
            messages.error(request, "No se pueden aplicar vacunas a mascotas inactivas")
            return redirect('detalle_mascota', pk=mascota_id)
    
    if request.method == 'POST':
        form = VacunaAplicadaForm(request.POST)
        if form.is_valid():
            mascota = form.cleaned_data['mascota']
            if not mascota.activa:
                messages.error(request, "No se pueden aplicar vacunas a mascotas inactivas")
                return redirect('detalle_mascota', pk=mascota.id)
            
            vacuna_aplicada = form.save()
            messages.success(request, f"Vacuna {vacuna_aplicada.vacuna.nombre} aplicada correctamente a {vacuna_aplicada.mascota.nombre}")
            
            # Redireccionar a la mascota o a otra página
            return redirect('detalle_mascota', pk=vacuna_aplicada.mascota.id)
    else:
        initial_data = {}
        if mascota_inicial:
            initial_data['mascota'] = mascota_inicial
        
        form = VacunaAplicadaForm(initial=initial_data)
    
    context = {'form': form}
    if mascota_inicial:
        context['mascota'] = mascota_inicial
    
    return render(request, 'inventario/aplicar_vacuna.html', context)

@login_required
def lista_vacunas_aplicadas(request):
    # Filtramos por mascota si se proporciona
    mascota_id = request.GET.get('mascota_id')
    
    vacunas_aplicadas = VacunaAplicada.objects.all().order_by('-fecha_aplicacion')
    
    if mascota_id:
        vacunas_aplicadas = vacunas_aplicadas.filter(mascota_id=mascota_id)
    
    paginator = Paginator(vacunas_aplicadas, 20)
    page = request.GET.get('page')
    vacunas_paginadas = paginator.get_page(page)
    
    context = {'vacunas_aplicadas': vacunas_paginadas}
    if mascota_id:
        context['mascota'] = get_object_or_404(Mascota, pk=mascota_id)
    
    return render(request, 'inventario/lista_vacunas_aplicadas.html', context)

# ----- PRODUCTOS -----
@login_required
def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    
    return render(request, 'inventario/lista_productos.html', {
        'productos': productos
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f"Producto {producto.nombre} creado correctamente")
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f"Producto {producto.nombre} actualizado correctamente")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {
        'form': form,
        'producto': producto
    })

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto {nombre} eliminado correctamente")
        return redirect('lista_productos')
    
    return render(request, 'inventario/eliminar_producto.html', {
        'producto': producto
    })

# ----- PRODUCTOS APLICADOS -----
@login_required
def aplicar_producto(request, mascota_id=None):
    mascota_inicial = None
    if mascota_id:
        mascota_inicial = get_object_or_404(Mascota, pk=mascota_id)
        # Verificar que la mascota esté activa
        if not mascota_inicial.activa:
            messages.error(request, "No se pueden aplicar productos a mascotas inactivas")
            return redirect('detalle_mascota', pk=mascota_id)
    
    if request.method == 'POST':
        form = ProductoAplicadoForm(request.POST)
        if form.is_valid():
            mascota = form.cleaned_data['mascota']
            if not mascota.activa:
                messages.error(request, "No se pueden aplicar productos a mascotas inactivas")
                return redirect('detalle_mascota', pk=mascota.id)
            
            producto_aplicado = form.save()
            messages.success(request, f"Producto {producto_aplicado.producto.nombre} aplicado correctamente a {producto_aplicado.mascota.nombre}")
            
            # Redireccionar a la mascota
            return redirect('detalle_mascota', pk=producto_aplicado.mascota.id)
    else:
        initial_data = {}
        if mascota_inicial:
            initial_data['mascota'] = mascota_inicial
        
        form = ProductoAplicadoForm(initial=initial_data)
    
    context = {'form': form}
    if mascota_inicial:
        context['mascota'] = mascota_inicial
    
    return render(request, 'inventario/aplicar_producto.html', context)

@login_required
def lista_productos_aplicados(request):
    # Filtramos por mascota si se proporciona
    mascota_id = request.GET.get('mascota_id')
    
    productos_aplicados = ProductoAplicado.objects.all().order_by('-fecha_aplicacion')
    
    if mascota_id:
        productos_aplicados = productos_aplicados.filter(mascota_id=mascota_id)
    
    paginator = Paginator(productos_aplicados, 20)
    page = request.GET.get('page')
    productos_paginados = paginator.get_page(page)
    
    context = {'productos_aplicados': productos_paginados}
    if mascota_id:
        context['mascota'] = get_object_or_404(Mascota, pk=mascota_id)
    
    return render(request, 'inventario/lista_productos_aplicados.html', context)

#----------------------------------- BLOQUE A DISCUTIR ------------------------------------------------------------
class VacunaListView(LoginRequiredMixin, ListView):
    model = Vacuna
    template_name = 'inventario/vacuna_list.html'
    context_object_name = 'vacunas'
    paginate_by = 10

class VacunaCreateView(LoginRequiredMixin, CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'inventario/vacuna_form.html'
    success_url = reverse_lazy('vacuna-list')

class VacunaUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'inventario/vacuna_form.html'
    success_url = reverse_lazy('vacuna-list')

class VacunaDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacuna
    template_name = 'inventario/vacuna_confirm_delete.html'
    success_url = reverse_lazy('vacuna-list')

class VacunaAplicadaCreateView(LoginRequiredMixin, CreateView):
    model = VacunaAplicada
    form_class = VacunaAplicadaForm
    template_name = 'inventario/vacuna_aplicada_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'mascota_id' in self.kwargs:
            initial['mascota'] = self.kwargs['mascota_id']
        return initial
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])

class VacunaAplicadaUpdateView(LoginRequiredMixin, UpdateView):
    model = VacunaAplicada
    form_class = VacunaAplicadaForm
    template_name = 'inventario/vacuna_aplicada_form.html'
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])

class VacunaAplicadaDeleteView(LoginRequiredMixin, DeleteView):
    model = VacunaAplicada
    template_name = 'inventario/vacuna_aplicada_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto-list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto-list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')

class ProductoAplicadoCreateView(LoginRequiredMixin, CreateView):
    model = ProductoAplicado
    form_class = ProductoAplicadoForm
    template_name = 'inventario/producto_aplicado_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'mascota_id' in self.kwargs:
            initial['mascota'] = self.kwargs['mascota_id']
        return initial
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])

class ProductoAplicadoUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductoAplicado
    form_class = ProductoAplicadoForm
    template_name = 'inventario/producto_aplicado_form.html'
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])

class ProductoAplicadoDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductoAplicado
    template_name = 'inventario/producto_aplicado_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('mascota-detail', args=[self.object.mascota.pk])