from django.db import models

class Especie(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
        ordering = ['nombre']

class Raza(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name='razas')
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.especie.nombre})"
    
    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"
        ordering = ['especie', 'nombre']
        unique_together = ['nombre', 'especie']  # No puede haber dos razas con el mismo nombre para la misma especie