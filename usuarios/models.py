from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    avatar = models.ImageField(upload_to='perfiles/', blank=True, null=True, verbose_name="Avatar")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    def __str__(self):
        nombre_completo = f"{self.user.first_name} {self.user.last_name}".strip()
        if nombre_completo:
            return f"Perfil de {nombre_completo}"
        return f"Perfil de {self.user.username}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario o el username si no hay nombre"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username
    
    @property
    def iniciales(self):
        """Retorna las iniciales del usuario para el avatar"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        elif self.user.first_name:
            return self.user.first_name[0].upper()
        else:
            return self.user.username[0].upper()
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"


# Signal para crear automáticamente el perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except PerfilUsuario.DoesNotExist:
        PerfilUsuario.objects.create(user=instance)