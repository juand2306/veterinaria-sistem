# usuarios/management/commands/setup_demo.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from usuarios.models import PerfilUsuario
import os

class Command(BaseCommand):
    help = 'Configura datos demo para la veterinaria'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la creación aunque ya existan datos',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🏥 Configurando demo de veterinaria...'))
        
        # Verificar si ya existen datos
        if User.objects.exists() and not options['force']:
            self.stdout.write(
                self.style.WARNING('⚠️  Ya existen usuarios. Usa --force para sobrescribir.')
            )
            return

        with transaction.atomic():
            # Crear superusuario
            self.crear_usuarios()
            
            # Crear datos demo (cuando me digas los modelos)
            # self.crear_datos_demo()
            
        self.stdout.write(self.style.SUCCESS('✅ Demo configurado exitosamente!'))
        self.mostrar_credenciales()

    def crear_usuarios(self):
        """Crea usuarios demo con sus perfiles"""
        # Superusuario admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@veterinaria.demo',
                password='veterinaria123',
                first_name='Admin',
                last_name='Sistema'
            )
            # El perfil se crea automáticamente por el signal
            admin.perfil.cargo = 'Administrador del Sistema'
            admin.perfil.telefono = '555-0001'
            admin.perfil.save()
            self.stdout.write(f'👤 Superusuario creado: {admin.username}')

        # Usuario veterinario demo
        if not User.objects.filter(username='veterinario').exists():
            vet = User.objects.create_user(
                username='veterinario',
                email='vet@veterinaria.demo',
                password='veterinaria123',
                first_name='Dr. Juan',
                last_name='Pérez'
            )
            vet.perfil.cargo = 'Veterinario Principal'
            vet.perfil.telefono = '555-0002'
            vet.perfil.save()
            self.stdout.write(f'👨‍⚕️ Veterinario creado: {vet.username}')

        # Usuario recepcionista demo
        if not User.objects.filter(username='recepcion').exists():
            recep = User.objects.create_user(
                username='recepcion',
                email='recepcion@veterinaria.demo',
                password='veterinaria123',
                first_name='María',
                last_name='González'
            )
            recep.perfil.cargo = 'Recepcionista'
            recep.perfil.telefono = '555-0003'
            recep.perfil.save()
            self.stdout.write(f'👩‍💼 Recepcionista creado: {recep.username}')

        # Usuario asistente demo
        if not User.objects.filter(username='asistente').exists():
            asist = User.objects.create_user(
                username='asistente',
                email='asistente@veterinaria.demo',
                password='veterinaria123',
                first_name='Carlos',
                last_name='López'
            )
            asist.perfil.cargo = 'Asistente Veterinario'
            asist.perfil.telefono = '555-0004'
            asist.perfil.save()
            self.stdout.write(f'🩺 Asistente creado: {asist.username}')

    def crear_datos_demo(self):
        """Crea datos demo de la veterinaria"""
        # Aquí vas a agregar la creación de:
        # - Clientes demo
        # - Mascotas demo  
        # - Citas demo
        # - Historiales demo
        # etc.
        pass

    def mostrar_credenciales(self):
        """Muestra las credenciales de acceso"""
        self.stdout.write(self.style.SUCCESS('\n🔑 CREDENCIALES DEMO:'))
        self.stdout.write('👤 Admin: admin / veterinaria123')
        self.stdout.write('👨‍⚕️ Veterinario: veterinario / veterinaria123') 
        self.stdout.write('👩‍💼 Recepción: recepcion / veterinaria123')
        self.stdout.write('🩺 Asistente: asistente / veterinaria123')
        self.stdout.write(self.style.WARNING('\n⚠️  Cambiar passwords en producción!'))
        self.stdout.write(self.style.SUCCESS('\n🌐 Ahora puedes acceder al sistema con cualquiera de estos usuarios'))
