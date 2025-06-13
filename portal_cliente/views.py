from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import AccesoCliente
from clientes.models import Cliente, Mascota
from .forms import LoginPortalForm, AccesoClienteForm
from clientes.models import Mascota
from consultas.models import Cita, Consulta, ImagenDiagnostica
from consultas.forms import CitaForm, ConsultaForm, ImagenDiagnosticaForm
from inventario.models import VacunaAplicada, ProductoAplicado
from django.db.models import Q

class PortalClienteMixin:
    """Mixin para verificar que el cliente esté logueado en el portal"""
    
    def dispatch(self, request, *args, **kwargs):
        if 'cliente_id' not in request.session:
            return redirect('portal_cliente:login')
        
        try:
            self.cliente_actual = Cliente.objects.get(id=request.session['cliente_id'])
        except Cliente.DoesNotExist:
            del request.session['cliente_id']
            return redirect('portal_cliente:login')
        
        return super().dispatch(request, *args, **kwargs)


class PortalLoginView(View):
    """Vista de login para clientes del portal"""
    
    def get(self, request):
        # Si ya está logueado, redirigir al dashboard
        if 'cliente_id' in request.session:
            return redirect('portal_cliente:dashboard')
        
        form = LoginPortalForm()
        return render(request, 'portal_cliente/login.html', {'form': form})
    
    def post(self, request):
        form = LoginPortalForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                acceso = AccesoCliente.objects.get(username=username, activo=True)
                
                if acceso.check_password(password):
                    # Login exitoso
                    request.session['cliente_id'] = acceso.cliente.id
                    request.session['cliente_username'] = acceso.username
                    
                    # Actualizar último acceso
                    acceso.actualizar_ultimo_acceso()
                    
                    messages.success(request, f'Bienvenido/a {acceso.cliente.nombre}')
                    return redirect('portal_cliente:dashboard')
                else:
                    messages.error(request, 'Credenciales incorrectas')
            
            except AccesoCliente.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas')
        
        return render(request, 'portal_cliente/login.html', {'form': form})


class PortalLogoutView(View):
    """Cerrar sesión del portal"""
    
    def get(self, request):
        if 'cliente_id' in request.session:
            del request.session['cliente_id']
        if 'cliente_username' in request.session:
            del request.session['cliente_username']
        
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('portal_cliente:login')


class PortalDashboardView(PortalClienteMixin, TemplateView):
    """Dashboard principal del cliente - Ver sus mascotas"""
    template_name = 'portal_cliente/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.cliente_actual
        context['mascotas'] = self.cliente_actual.mascotas.filter(activa=True).order_by('nombre')
        return context

class PortalHistoriaClinicaView(PortalClienteMixin, TemplateView):
    """Ver historia clínica de una mascota específica"""
    template_name = 'portal_cliente/historia_clinica.html'
    
    def get(self, request, mascota_id):
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        
        # Obtener consultas con select_related para optimizar
        consultas = Consulta.objects.filter(
            cita__mascota=mascota
        ).select_related('cita').order_by('-cita__fecha')
        
        # Obtener vacunas aplicadas
        vacunas_aplicadas = VacunaAplicada.objects.filter(
            mascota=mascota
        ).select_related('vacuna').order_by('-fecha_aplicacion')
        
        # Obtener productos aplicados
        productos_aplicados = ProductoAplicado.objects.filter(
            mascota=mascota
        ).select_related('producto').order_by('-fecha_aplicacion')
        
        # Obtener imágenes diagnósticas
        imagenes_diagnosticas = ImagenDiagnostica.objects.filter(
            mascota=mascota
        ).order_by('-fecha')
        
        # Obtener próximas citas (no atendidas y fecha futura)
        proximas_citas = Cita.objects.filter(
            mascota=mascota,
            fecha__gte=timezone.now(),  # Solo citas futuras
            atendida=False  # Solo citas no atendidas
        ).order_by('fecha')[:5]  # Limitar a las próximas 5 citas
        
        # Crear línea de tiempo unificada
        eventos = self.get_unified_timeline(consultas, vacunas_aplicadas, productos_aplicados, imagenes_diagnosticas)
        
        context = {
            'mascota': mascota,
            'consultas': consultas,
            'vacunas_aplicadas': vacunas_aplicadas,
            'productos_aplicados': productos_aplicados,
            'imagenes_diagnosticas': imagenes_diagnosticas,
            'eventos': eventos,
            'proximas_citas': proximas_citas,
        }
        return render(request, self.template_name, context)
    
    def get_unified_timeline(self, consultas, vacunas_aplicadas, productos_aplicados, imagenes_diagnosticas):
        eventos = []

        # Agregar consultas
        for consulta in consultas:
            # Convertir datetime a date para comparación consistente
            fecha = consulta.cita.fecha.date() if hasattr(consulta.cita.fecha, 'date') else consulta.cita.fecha
            eventos.append({
                'fecha': fecha,
                'tipo': 'consulta',
                'objeto': consulta,
                'titulo': f'Consulta - {consulta.cita.fecha.strftime("%d/%m/%Y")}'
            })
        
        # Agregar vacunas
        for vacuna in vacunas_aplicadas:
            # fecha_aplicacion ya debería ser date, pero verificamos por seguridad
            fecha = vacuna.fecha_aplicacion.date() if hasattr(vacuna.fecha_aplicacion, 'date') else vacuna.fecha_aplicacion
            eventos.append({
                'fecha': fecha,
                'tipo': 'vacuna',
                'objeto': vacuna,
                'titulo': f'Vacuna: {vacuna.vacuna.nombre}'
            })
        
        # Agregar productos
        for producto in productos_aplicados:
            # fecha_aplicacion ya debería ser date, pero verificamos por seguridad
            fecha = producto.fecha_aplicacion.date() if hasattr(producto.fecha_aplicacion, 'date') else producto.fecha_aplicacion
            eventos.append({
                'fecha': fecha,
                'tipo': 'producto',
                'objeto': producto,
                'titulo': f'Producto: {producto.producto.nombre}'
            })
            
        # Agregar imágenes diagnósticas
        for imagen in imagenes_diagnosticas:
            # Manejar tanto date como datetime
            fecha = imagen.fecha.date() if hasattr(imagen.fecha, 'date') else imagen.fecha
            eventos.append({
                'fecha': fecha,
                'tipo': 'imagen',
                'objeto': imagen,
                'titulo': f'Imagen diagnóstica: {imagen.descripcion[:50]}...'
            })
        
        # Ordenar por fecha descendente
        eventos.sort(key=lambda x: x['fecha'], reverse=True)
        return eventos
    
def historia_clinica_imprimible(request, mascota_id):
    """
    Vista para generar la versión imprimible de la historia clínica
    """
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Obtener todos los datos relacionados
    consultas = Consulta.objects.filter(
        cita__mascota=mascota
    ).select_related('cita').order_by('-cita__fecha')
    
    vacunas_aplicadas = VacunaAplicada.objects.filter(
        mascota=mascota
    ).select_related('vacuna').order_by('-fecha_aplicacion')
    
    productos_aplicados = ProductoAplicado.objects.filter(
        mascota=mascota
    ).select_related('producto').order_by('-fecha_aplicacion')
    
    imagenes_diagnosticas = ImagenDiagnostica.objects.filter(
        mascota=mascota
    ).order_by('-fecha')
    
    context = {
        'mascota': mascota,
        'consultas': consultas,
        'vacunas_aplicadas': vacunas_aplicadas,
        'productos_aplicados': productos_aplicados,
        'imagenes_diagnosticas': imagenes_diagnosticas,
    }
    
    return render(request, 'portal_cliente/historia_clinica_print.html', context)


class PortalHistoriaClinicaImprimibleView(DetailView):
    """
    Vista basada en clase para la historia clínica imprimible
    """
    model = Mascota
    template_name = 'portal_cliente/historia_clinica_print.html'
    context_object_name = 'mascota'
    pk_url_kwarg = 'mascota_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mascota = self.get_object()
        
        # Obtener historial médico
        context['consultas'] = Consulta.objects.filter(
            cita__mascota=mascota
        ).select_related('cita').order_by('-cita__fecha')
        
        context['vacunas_aplicadas'] = VacunaAplicada.objects.filter(
            mascota=mascota
        ).select_related('vacuna').order_by('-fecha_aplicacion')
        
        context['productos_aplicados'] = ProductoAplicado.objects.filter(
            mascota=mascota
        ).select_related('producto').order_by('-fecha_aplicacion')
        
        context['imagenes_diagnosticas'] = ImagenDiagnostica.objects.filter(
            mascota=mascota
        ).order_by('-fecha')
        
        return context


# ==================== VISTAS PARA ADMINISTRACIÓN (PERSONAL VETERINARIA) ====================

class ListaAccesosView(LoginRequiredMixin, ListView):
    """Lista todos los accesos creados para clientes"""
    model = AccesoCliente
    template_name = 'portal_cliente/lista_accesos.html'
    context_object_name = 'accesos'
    paginate_by = 20
    
    def get_queryset(self):
        # Queryset base
        queryset = AccesoCliente.objects.select_related('cliente').order_by('-fecha_creacion')
        
        # Obtener parámetros de búsqueda
        buscar = self.request.GET.get('buscar', '').strip()
        estado = self.request.GET.get('estado', '').strip()
        
        # Aplicar filtro de búsqueda por nombre, usuario o email
        if buscar:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=buscar) |
                Q(username__icontains=buscar) |
                Q(cliente__correo__icontains=buscar)
            )
        
        # Aplicar filtro por estado
        if estado:
            if estado == 'activo':
                queryset = queryset.filter(activo=True)
            elif estado == 'inactivo':
                queryset = queryset.filter(activo=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pasar los parámetros de búsqueda al template
        context['buscar'] = self.request.GET.get('buscar', '')
        context['estado'] = self.request.GET.get('estado', '')
        
        return context


class CrearAccesoClienteView(LoginRequiredMixin, CreateView):
    """Crear acceso web para un cliente específico"""
    model = AccesoCliente
    form_class = AccesoClienteForm
    template_name = 'portal_cliente/crear_acceso.html'
    success_url = reverse_lazy('portal_cliente:lista_accesos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_id = self.kwargs.get('cliente_id')
        context['cliente'] = get_object_or_404(Cliente, id=cliente_id)
        
        # Verificar si ya tiene acceso
        if hasattr(context['cliente'], 'acceso_portal'):
            context['ya_tiene_acceso'] = True
        
        return context
    
    def form_valid(self, form):
        cliente_id = self.kwargs.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        # Verificar que no tenga acceso ya
        if hasattr(cliente, 'acceso_portal'):
            messages.error(self.request, 'Este cliente ya tiene acceso al portal')
            return redirect('portal_cliente:lista_accesos')
        
        form.instance.cliente = cliente
        
        # Encriptar contraseña antes de guardar
        raw_password = form.cleaned_data['password']
        
        response = super().form_valid(form)
        
        # Encriptar después de crear el objeto
        self.object.set_password(raw_password)
        self.object.save()
        
        messages.success(
            self.request, 
            f'Acceso creado exitosamente para {cliente.nombre}. '
            f'Usuario: {self.object.username}'
        )
        
        return response
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = False  # Indicar que es creación
        return kwargs


class EditarAccesoClienteView(LoginRequiredMixin, UpdateView):
    """Editar acceso existente"""
    model = AccesoCliente
    form_class = AccesoClienteForm
    template_name = 'portal_cliente/editar_acceso.html'
    success_url = reverse_lazy('portal_cliente:lista_accesos')
    pk_url_kwarg = 'acceso_id'
    
    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        
        # Solo cambiar la contraseña si se proporcionó una nueva
        if password:
            response = super().form_valid(form)
            self.object.set_password(password)
            self.object.save()
            messages.success(self.request, 'Acceso actualizado correctamente (incluyendo contraseña)')
            return response
        else:
            messages.success(self.request, 'Acceso actualizado correctamente')
            return super().form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit'] = True  # Indicar que es edición
        return kwargs


class EliminarAccesoClienteView(LoginRequiredMixin, DeleteView):
    """Eliminar acceso de cliente"""
    model = AccesoCliente
    template_name = 'portal_cliente/eliminar_acceso.html'
    success_url = reverse_lazy('portal_cliente:lista_accesos')
    pk_url_kwarg = 'acceso_id'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Acceso eliminado correctamente')
        return response