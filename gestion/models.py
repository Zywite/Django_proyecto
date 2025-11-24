from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Incluye campos adicionales como rol, teléfono, nombre y apellido.
    """

    nombre = models.CharField(max_length=100, default="")
    apellido = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ROL_CHOICES = (
        ("administrador", "Administrador"),
        ("cliente", "Cliente"),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="cliente")


class Habitacion(models.Model):
    """
    Representa una habitación en el albergue.
    """

    TIPO_CHOICES = (
        ("individual", "Individual"),
        ("doble", "Doble"),
        ("suite", "Suite"),
    )
    ESTADO_CHOICES = (
        ("disponible", "Disponible"),
        ("ocupada", "Ocupada"),
        ("mantenimiento", "Mantenimiento"),
    )
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="disponible"
    )

    def __str__(self):
        return f"Habitación {self.numero} ({self.tipo})"


class Reserva(models.Model):
    """
    Representa una reserva de una habitación por un usuario.
    Incluye validación para evitar superposición de fechas.
    """

    ESTADO_CHOICES = (
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="pendiente"
    )

    def clean(self):
        """
        Valida que la fecha de fin sea posterior a la de inicio
        y que no existan reservas superpuestas para la misma habitación.
        """
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de inicio."
                )

            reservas_superpuestas = (
                Reserva.objects.filter(
                    habitacion=self.habitacion, estado__in=["pendiente", "confirmada"]
                )
                .filter(
                    Q(fecha_inicio__range=(self.fecha_inicio, self.fecha_fin))
                    | Q(fecha_fin__range=(self.fecha_inicio, self.fecha_fin))
                    | Q(
                        fecha_inicio__lte=self.fecha_inicio,
                        fecha_fin__gte=self.fecha_fin,
                    )
                )
                .exclude(pk=self.pk)
            )

            if reservas_superpuestas.exists():
                raise ValidationError(
                    f"La habitación {self.habitacion.numero} ya está reservada en estas fechas."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.habitacion}"


class Clima(models.Model):
    """
    Almacena información del clima para una fecha específica.
    """

    fecha = models.DateField(unique=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    probabilidad_lluvia = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Clima para {self.fecha}"


class Recurso(models.Model):
    """
    Representa un recurso o insumo del albergue (ej. jabón, toallas).
    """

    TIPO_CHOICES = (
        ("consumible", "Consumible"),
        ("reutilizable", "Reutilizable"),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad_total = models.IntegerField()
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class MovimientoRecurso(models.Model):
    """
    Registra los movimientos (ingresos o egresos) de stock de un recurso.
    Actualiza automáticamente la cantidad total del recurso al guardarse.
    """

    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    motivo = models.TextField()

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para actualizar el stock del recurso asociado
        cuando se crea un nuevo movimiento.
        """
        if not self.pk:
            self.recurso.cantidad_total += self.cantidad
            self.recurso.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Movimiento de {self.recurso.nombre}: {self.cantidad}"


class Contacto(models.Model):
    """
    Almacena mensajes de contacto enviados por los usuarios.
    """

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.fecha})"
