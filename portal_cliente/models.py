from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone



class AccesoCliente(models.Model):
    cliente = models.OneToOneField('clientes.Cliente', on_delete=models.CASCADE, related_name='acceso_portal')
    username = models.CharField(max_length=50, unique=True, verbose_name='Usuario')
    password = models.CharField(max_length=128, verbose_name='Contraseña')  # Para hash
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_ultimo_acceso = models.DateTimeField(null=True, blank=True, verbose_name='Último acceso')
    
    class Meta:
        verbose_name = 'Acceso Portal Cliente'
        verbose_name_plural = 'Accesos Portal Clientes'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.username} - {self.cliente.nombre}"
    
    def set_password(self, raw_password):
        """Encripta y guarda la contraseña"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verifica la contraseña"""
        return check_password(raw_password, self.password)
    
    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha del último acceso"""
        self.fecha_ultimo_acceso = timezone.now()
        self.save(update_fields=['fecha_ultimo_acceso'])