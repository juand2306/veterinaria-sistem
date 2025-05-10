from django.contrib import admin
from .models import Cita, Consulta, ImagenDiagnostica

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'fecha', 'motivo', 'programada')
    list_filter = ('programada', 'fecha')
    search_fields = ('mascota__nombre', 'motivo')
    date_hierarchy = 'fecha'

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('cita', 'fecha_consulta', 'diagnostico', 'es_eutanasia')
    list_filter = ('es_eutanasia', 'fecha_consulta')
    search_fields = ('cita__mascota__nombre', 'diagnostico', 'tratamiento')
    date_hierarchy = 'fecha_consulta'

@admin.register(ImagenDiagnostica)
class ImagenDiagnosticaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'descripcion', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('mascota__nombre', 'descripcion')
    date_hierarchy = 'fecha'