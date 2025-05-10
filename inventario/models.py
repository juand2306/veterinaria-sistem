from django.db import models
from clientes.models import Mascota

class Vacuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['nombre']

class VacunaAplicada(models.Model):
    mascota = models.ForeignKey('clientes.Mascota', on_delete=models.CASCADE, related_name='vacunas_aplicadas')
    vacuna = models.ForeignKey(Vacuna, on_delete=models.PROTECT)
    fecha_aplicacion = models.DateField()
    fecha_proxima = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.vacuna.nombre} - {self.mascota.nombre} ({self.fecha_aplicacion.strftime('%d/%m/%Y')})"
    
    def save(self, *args, **kwargs):
        # Verificar que la mascota esté activa
        if not self.mascota.activa and not self.id:  # Solo para nuevos registros
            raise ValueError("No se pueden aplicar vacunas a mascotas inactivas")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Vacuna Aplicada"
        verbose_name_plural = "Vacunas Aplicadas"
        ordering = ['-fecha_aplicacion']

class Producto(models.Model):
    TIPO_CHOICES = [
        ('V', 'Vermífugo'),
        ('A', 'Antiparasitario'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

class ProductoAplicado(models.Model):
    mascota = models.ForeignKey('clientes.Mascota', on_delete=models.CASCADE, related_name='productos_aplicados')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    fecha_aplicacion = models.DateField()
    fecha_proxima = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.mascota.nombre} ({self.fecha_aplicacion.strftime('%d/%m/%Y')})"
    
    def save(self, *args, **kwargs):
        # Verificar que la mascota esté activa
        if not self.mascota.activa and not self.id:  # Solo para nuevos registros
            raise ValueError("No se pueden aplicar productos a mascotas inactivas")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Producto Aplicado"
        verbose_name_plural = "Productos Aplicados"
        ordering = ['-fecha_aplicacion']