from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fields = ('telefono', 'cargo', 'avatar')

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_telefono', 'get_cargo')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_telefono(self, obj):
        return obj.perfil.telefono if hasattr(obj, 'perfil') and obj.perfil.telefono else '-'
    get_telefono.short_description = 'Teléfono'
    
    def get_cargo(self, obj):
        return obj.perfil.cargo if hasattr(obj, 'perfil') and obj.perfil.cargo else '-'
    get_cargo.short_description = 'Cargo'

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'cargo', 'fecha_actualizacion')
    list_filter = ('cargo', 'fecha_actualizacion')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telefono')
    readonly_fields = ('fecha_actualizacion',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)