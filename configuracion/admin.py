from django.contrib import admin
from .models import Especie, Raza

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'descripcion')
    list_filter = ('especie',)
    search_fields = ('nombre', 'especie__nombre')