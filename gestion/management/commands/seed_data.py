
import datetime
from django.core.management.base import BaseCommand
from gestion.models import Usuario, Habitacion, Recurso, Clima, Reserva, MovimientoRecurso

class Command(BaseCommand):
    help = 'Crea datos de prueba para el albergue'

    def handle(self, *args, **kwargs):
        self.stdout.write('Limpiando la base de datos...')
        # Limpiar datos existentes para evitar duplicados
        Usuario.objects.all().delete()
        Habitacion.objects.all().delete()
        Recurso.objects.all().delete()
        Clima.objects.all().delete()
        Reserva.objects.all().delete()
        MovimientoRecurso.objects.all().delete()

        self.stdout.write('Creando usuarios...')
        admin = Usuario.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        admin.rol = 'administrador'
        admin.save()

        cliente = Usuario.objects.create_user('cliente', 'cliente@example.com', 'clientepass')
        cliente.rol = 'cliente'
        cliente.save()

        self.stdout.write('Creando habitaciones...')
        h101 = Habitacion.objects.create(numero='101', tipo='individual', capacidad=1, precio=50.00)
        h102 = Habitacion.objects.create(numero='102', tipo='doble', capacidad=2, precio=80.00)
        h201 = Habitacion.objects.create(numero='201', tipo='suite', capacidad=4, precio=150.00, estado='mantenimiento')

        self.stdout.write('Creando recursos...')
        jabon = Recurso.objects.create(nombre='Jabón', tipo='consumible', cantidad_total=100, unidad='unidades')
        toallas = Recurso.objects.create(nombre='Toallas', tipo='reutilizable', cantidad_total=50, unidad='unidades')

        self.stdout.write('Creando datos de clima...')
        today = datetime.date.today()
        Clima.objects.create(fecha=today, temperatura=25.5, probabilidad_lluvia=10)
        Clima.objects.create(fecha=today + datetime.timedelta(days=1), temperatura=22.0, probabilidad_lluvia=40)

        self.stdout.write('Creando una reserva de prueba...')
        Reserva.objects.create(
            usuario=cliente,
            habitacion=h101,
            fecha_inicio=today + datetime.timedelta(days=5),
            fecha_fin=today + datetime.timedelta(days=10),
            estado='confirmada'
        )

        self.stdout.write('Creando un movimiento de recurso...')
        MovimientoRecurso.objects.create(recurso=jabon, cantidad=-10, motivo='Uso en habitaciones')

        self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados exitosamente!'))
