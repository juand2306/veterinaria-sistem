from django.contrib import admin
from .models import Cliente, Mascota

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo', 'direccion', 'fecha_registro')
    search_fields = ('nombre', 'telefono', 'correo')
    list_filter = ('fecha_registro',)

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'especie', 'raza', 'sexo', 'fecha_nacimiento', 'activa')
    list_filter = ('especie', 'raza', 'sexo', 'activa')
    search_fields = ('nombre', 'cliente__nombre')
    date_hierarchy = 'fecha_nacimiento'