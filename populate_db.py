import os
import django
import random
from datetime import date, timedelta

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albergue_project.settings')
django.setup()

from gestion.models import Usuario, Habitacion, Reserva, Recurso, Clima, MovimientoRecurso

def populate():
    print("Iniciando script de población de datos...")

    # 1. Crear Usuarios
    print("Creando usuarios...")
    usuarios_data = [
        {'username': 'admin_user', 'email': 'admin@example.com', 'rol': 'administrador', 'nombre': 'Admin', 'apellido': 'Principal'},
        {'username': 'cliente1', 'email': 'cliente1@example.com', 'rol': 'cliente', 'nombre': 'Juan', 'apellido': 'Perez'},
        {'username': 'cliente2', 'email': 'cliente2@example.com', 'rol': 'cliente', 'nombre': 'Maria', 'apellido': 'Gomez'},
        {'username': 'cliente3', 'email': 'cliente3@example.com', 'rol': 'cliente', 'nombre': 'Carlos', 'apellido': 'Lopez'},
    ]

    usuarios_objs = []
    for u_data in usuarios_data:
        if not Usuario.objects.filter(username=u_data['username']).exists():
            user = Usuario.objects.create_user(
                username=u_data['username'],
                email=u_data['email'],
                password='password123',
                rol=u_data['rol'],
                nombre=u_data['nombre'],
                apellido=u_data['apellido']
            )
            usuarios_objs.append(user)
            print(f"Usuario creado: {user.username}")
        else:
            usuarios_objs.append(Usuario.objects.get(username=u_data['username']))
            print(f"Usuario ya existe: {u_data['username']}")

    # 2. Crear Habitaciones
    print("Creando habitaciones...")
    tipos = ['individual', 'doble', 'suite']
    estados = ['disponible', 'ocupada', 'mantenimiento']
    
    for i in range(101, 111): # 10 habitaciones
        numero = str(i)
        if not Habitacion.objects.filter(numero=numero).exists():
            tipo = random.choice(tipos)
            capacidad = 1 if tipo == 'individual' else (2 if tipo == 'doble' else 4)
            precio = 50.00 if tipo == 'individual' else (80.00 if tipo == 'doble' else 150.00)
            
            Habitacion.objects.create(
                numero=numero,
                tipo=tipo,
                capacidad=capacidad,
                precio=precio,
                estado=random.choice(estados)
            )
            print(f"Habitación creada: {numero}")

    habitaciones = list(Habitacion.objects.all())

    # 3. Crear Reservas
    print("Creando reservas...")
    clientes = [u for u in usuarios_objs if u.rol == 'cliente']
    if clientes and habitaciones:
        for _ in range(10):
            usuario = random.choice(clientes)
            habitacion = random.choice(habitaciones)
            start_date = date.today() + timedelta(days=random.randint(-10, 30))
            end_date = start_date + timedelta(days=random.randint(1, 7))
            
            Reserva.objects.create(
                usuario=usuario,
                habitacion=habitacion,
                fecha_inicio=start_date,
                fecha_fin=end_date,
                estado=random.choice(['pendiente', 'confirmada', 'cancelada'])
            )
    print("Reservas creadas.")

    # 4. Crear Recursos
    print("Creando recursos...")
    recursos_data = [
        {'nombre': 'Jabón', 'tipo': 'consumible', 'unidad': 'unidades'},
        {'nombre': 'Toallas', 'tipo': 'reutilizable', 'unidad': 'unidades'},
        {'nombre': 'Papel Higiénico', 'tipo': 'consumible', 'unidad': 'rollos'},
        {'nombre': 'Sábanas', 'tipo': 'reutilizable', 'unidad': 'juegos'},
        {'nombre': 'Detergente', 'tipo': 'consumible', 'unidad': 'litros'},
    ]

    recursos_objs = []
    for r_data in recursos_data:
        recurso, created = Recurso.objects.get_or_create(
            nombre=r_data['nombre'],
            defaults={
                'tipo': r_data['tipo'],
                'cantidad_total': random.randint(10, 100),
                'unidad': r_data['unidad']
            }
        )
        recursos_objs.append(recurso)
        if created:
            print(f"Recurso creado: {recurso.nombre}")

    # 5. Crear Movimientos de Recursos
    print("Creando movimientos de recursos...")
    for _ in range(15):
        recurso = random.choice(recursos_objs)
        cantidad = random.randint(-5, 10)
        if cantidad == 0: cantidad = 1
        
        MovimientoRecurso.objects.create(
            recurso=recurso,
            cantidad=cantidad,
            motivo="Reposición" if cantidad > 0 else "Consumo diario"
        )
    print("Movimientos creados.")

    # 6. Crear Clima
    print("Creando datos del clima...")
    base_date = date.today()
    for i in range(7):
        fecha = base_date + timedelta(days=i)
        if not Clima.objects.filter(fecha=fecha).exists():
            Clima.objects.create(
                fecha=fecha,
                temperatura=random.uniform(15.0, 30.0),
                probabilidad_lluvia=random.randint(0, 100),
                comentarios="Día soleado" if random.random() > 0.5 else "Posibilidad de lluvia"
            )
    print("Datos del clima creados.")

    print("¡Población de datos completada con éxito!")

if __name__ == '__main__':
    populate()
