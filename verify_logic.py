import os
import django
from datetime import date, timedelta
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albergue_project.settings")
django.setup()


def verify():
    """
    Script de verificación de lógica de negocio.
    Prueba la validación de reservas superpuestas y la actualización automática de stock.
    """
    print("--- Verificando Lógica de Negocio ---")
    from gestion.models import Reserva, Habitacion, Usuario, Recurso, MovimientoRecurso

    print("\n1. Prueba de Reservas Superpuestas:")
    try:
        usuario = Usuario.objects.first()
        habitacion = Habitacion.objects.first()

        fecha_inicio = date.today() + timedelta(days=50)
        fecha_fin = date.today() + timedelta(days=55)

        print(f"Creando reserva base: {fecha_inicio} a {fecha_fin}")
        Reserva.objects.create(
            usuario=usuario,
            habitacion=habitacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado="confirmada",
        )
        print("Reserva base creada.")

        print("Intentando crear reserva superpuesta...")
        r2 = Reserva(
            usuario=usuario,
            habitacion=habitacion,
            fecha_inicio=fecha_inicio + timedelta(days=1),
            fecha_fin=fecha_fin + timedelta(days=1),
            estado="pendiente",
        )
        r2.save()
        print("ERROR: Se permitió crear una reserva superpuesta.")
    except ValidationError as e:
        print(f"ÉXITO: La validación funcionó. Error capturado: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")

    print("\n2. Prueba de Control de Stock:")
    recurso = Recurso.objects.first()
    stock_inicial = recurso.cantidad_total
    print(f"Recurso: {recurso.nombre}, Stock Inicial: {stock_inicial}")

    cantidad_movimiento = 10
    print(f"Registrando ingreso de {cantidad_movimiento} unidades...")
    MovimientoRecurso.objects.create(
        recurso=recurso, cantidad=cantidad_movimiento, motivo="Prueba de automatización"
    )

    recurso.refresh_from_db()
    stock_final = recurso.cantidad_total
    print(f"Stock Final: {stock_final}")

    if stock_final == stock_inicial + cantidad_movimiento:
        print("ÉXITO: El stock se actualizó correctamente.")
    else:
        print("ERROR: El stock no se actualizó correctamente.")


if __name__ == "__main__":
    verify()
