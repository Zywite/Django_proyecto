import os
import django
import random
from datetime import date, timedelta
from faker import Faker

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albergue_project.settings")
django.setup()

from gestion.models import (  # noqa: E402
    Usuario,
    Habitacion,
    Reserva,
    Recurso,
    Clima,
    MovimientoRecurso,
    Contacto,
)

fake = Faker("es_ES")


def clean_database():
    """
    Elimina todos los registros de la base de datos en orden correcto
    para evitar conflictos de claves foráneas.
    """
    print("Limpiando base de datos...")

    # Eliminar primero los modelos que tienen claves foráneas (Hijos)
    print("- Eliminando Movimientos de Recursos...")
    MovimientoRecurso.objects.all().delete()

    print("- Eliminando Reservas...")
    Reserva.objects.all().delete()

    # Eliminar modelos independientes o padres
    print("- Eliminando Recursos...")
    Recurso.objects.all().delete()

    print("- Eliminando Habitaciones...")
    Habitacion.objects.all().delete()

    print("- Eliminando Clima...")
    Clima.objects.all().delete()

    print("- Eliminando Contactos...")
    Contacto.objects.all().delete()

    # NO eliminamos usuarios para preservar los existentes
    # Usuario.objects.all().delete()

    print("Base de datos limpia (excepto usuarios).")


def populate():
    """
    Script para poblar la base de datos con datos de prueba usando Faker.
    """
    clean_database()
    print("Iniciando script de población de datos con Faker...")

    # --- USUARIOS ---
    print("Creando usuarios...")
    # Crear admin si no existe
    if not Usuario.objects.filter(username="Admin").exists():
        Usuario.objects.create_user(
            username="Admin",
            email="admin@gmail.com",
            password="Adminpass",
            rol="administrador",
            nombre="Admin",
            apellido="Principal",
        )
        print("Usuario admin creado.")

    # Crear clientes falsos
    usuarios_objs = []
    # Recuperar admin
    try:
        usuarios_objs.append(Usuario.objects.get(username="Admin"))
    except Usuario.DoesNotExist:
        pass

    # Recuperar otros usuarios existentes
    usuarios_existentes = Usuario.objects.all()
    if usuarios_existentes:
        usuarios_objs.extend(list(usuarios_existentes))

    # Crear algunos nuevos si hay pocos
    if len(usuarios_objs) < 10:
        for _ in range(5):
            username = fake.user_name()
            # Asegurar unicidad de username
            while Usuario.objects.filter(username=username).exists():
                username = fake.user_name() + str(random.randint(1, 999))

            email = fake.email()

            user = Usuario.objects.create_user(
                username=username,
                email=email,
                password="password123",
                rol="cliente",
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                telefono=fake.phone_number(),
            )
            usuarios_objs.append(user)
            print(f"Usuario creado: {username}")

    print(f"Total usuarios disponibles: {len(usuarios_objs)}")

    # --- HABITACIONES ---
    print("Creando habitaciones...")
    tipos = ["individual", "doble", "suite"]
    estados = ["disponible", "ocupada", "mantenimiento"]

    # Creamos habitaciones fijas (ej. 101-120)
    for i in range(101, 121):
        numero = str(i)
        if not Habitacion.objects.filter(numero=numero).exists():
            tipo = random.choice(tipos)
            capacidad = 1 if tipo == "individual" else (2 if tipo == "doble" else 4)
            precio = (
                50.00
                if tipo == "individual"
                else (80.00 if tipo == "doble" else 150.00)
            )

            Habitacion.objects.create(
                numero=numero,
                tipo=tipo,
                capacidad=capacidad,
                precio=precio,
                estado=random.choice(estados),
            )
    print("Habitaciones verificadas/creadas.")

    habitaciones = list(Habitacion.objects.all())
    # Filtrar solo clientes para reservas
    clientes = [u for u in usuarios_objs if u.rol == "cliente"]

    # --- RESERVAS ---
    print("Creando reservas...")
    if clientes and habitaciones:
        for _ in range(20):
            usuario = random.choice(clientes)
            habitacion = random.choice(habitaciones)

            # Fechas aleatorias en los próximos 2 meses o pasados
            start_date = fake.date_between(start_date="-1M", end_date="+2M")
            end_date = start_date + timedelta(days=random.randint(1, 7))

            # Intentar crear reserva (puede fallar por validación de solapamiento, lo manejamos)
            try:
                Reserva.objects.create(
                    usuario=usuario,
                    habitacion=habitacion,
                    fecha_inicio=start_date,
                    fecha_fin=end_date,
                    estado=random.choice(["pendiente", "confirmada", "cancelada"]),
                )
            except Exception:
                # Si choca con otra reserva, simplemente la ignoramos en este script de prueba
                continue
    print("Reservas generadas.")

    # --- RECURSOS ---
    print("Creando recursos...")
    recursos_data = [
        {"nombre": "Jabón", "tipo": "consumible", "unidad": "unidades"},
        {"nombre": "Toallas", "tipo": "reutilizable", "unidad": "unidades"},
        {"nombre": "Papel Higiénico", "tipo": "consumible", "unidad": "rollos"},
        {"nombre": "Sábanas", "tipo": "reutilizable", "unidad": "juegos"},
        {"nombre": "Detergente", "tipo": "consumible", "unidad": "litros"},
        {"nombre": "Champú", "tipo": "consumible", "unidad": "botes"},
        {"nombre": "Almohadas", "tipo": "reutilizable", "unidad": "unidades"},
    ]

    recursos_objs = []
    for r_data in recursos_data:
        recurso, created = Recurso.objects.get_or_create(
            nombre=r_data["nombre"],
            defaults={
                "tipo": r_data["tipo"],
                "cantidad_total": random.randint(20, 200),
                "unidad": r_data["unidad"],
            },
        )
        recursos_objs.append(recurso)

    # --- MOVIMIENTOS DE RECURSOS ---
    print("Creando movimientos de recursos...")
    motivos_recursos = [
        "Compra mensual de suministros",
        "Reposición de stock agotado",
        "Consumo diario de huéspedes",
        "Ajuste de inventario por merma",
        "Donación recibida",
        "Uso en limpieza de habitaciones",
        "Reemplazo por deterioro",
        "Compra de emergencia",
    ]
    for _ in range(30):
        recurso = random.choice(recursos_objs)
        cantidad = random.randint(-10, 20)
        if cantidad == 0:
            cantidad = 5

        MovimientoRecurso.objects.create(
            recurso=recurso, cantidad=cantidad, motivo=random.choice(motivos_recursos)
        )
    print("Movimientos generados.")

    # --- CLIMA ---
    print("Creando datos del clima...")
    comentarios_clima = [
        "Cielo despejado y soleado.",
        "Nublado con probabilidad de lluvia.",
        "Tormentas eléctricas por la tarde.",
        "Viento fuerte y descenso de temperatura.",
        "Día agradable con brisa suave.",
        "Lluvia ligera intermitente.",
        "Calor intenso, se recomienda hidratación.",
        "Fresco por la mañana, templado por la tarde.",
    ]
    base_date = date.today()
    for i in range(14):  # Próximas 2 semanas
        fecha = base_date + timedelta(days=i)
        if not Clima.objects.filter(fecha=fecha).exists():
            Clima.objects.create(
                fecha=fecha,
                temperatura=random.uniform(10.0, 35.0),
                probabilidad_lluvia=random.randint(0, 100),
                comentarios=random.choice(comentarios_clima),
            )
    print("Datos del clima generados.")

    # --- CONTACTO ---
    print("Creando mensajes de contacto...")
    for _ in range(10):
        Contacto.objects.create(
            nombre=fake.name(),
            email=fake.email(),
            mensaje=fake.text(),
        )
    print("Mensajes de contacto generados.")

    print("¡Población de datos con Faker completada con éxito!")


if __name__ == "__main__":
    populate()
