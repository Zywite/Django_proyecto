
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100, default='')
    apellido = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ROL_CHOICES = (
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

class Habitacion(models.Model):
    TIPO_CHOICES = (
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
    )
    ESTADO_CHOICES = (
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'Mantenimiento'),
    )
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        return f"Habitación {self.numero} ({self.tipo})"

class Reserva(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

            # Verificar superposición de reservas
            reservas_superpuestas = Reserva.objects.filter(
                habitacion=self.habitacion,
                estado__in=['pendiente', 'confirmada']
            ).filter(
                Q(fecha_inicio__range=(self.fecha_inicio, self.fecha_fin)) |
                Q(fecha_fin__range=(self.fecha_inicio, self.fecha_fin)) |
                Q(fecha_inicio__lte=self.fecha_inicio, fecha_fin__gte=self.fecha_fin)
            ).exclude(pk=self.pk) # Excluir la reserva actual si se está editando

            if reservas_superpuestas.exists():
                raise ValidationError(f"La habitación {self.habitacion.numero} ya está reservada en estas fechas.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.habitacion}"

class Clima(models.Model):
    fecha = models.DateField(unique=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    probabilidad_lluvia = models.IntegerField() # En porcentaje
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Clima para {self.fecha}"

class Recurso(models.Model):
    TIPO_CHOICES = (
        ('consumible', 'Consumible'),
        ('reutilizable', 'Reutilizable'),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad_total = models.IntegerField()
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class MovimientoRecurso(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField() # Positivo para ingreso, negativo para gasto
    motivo = models.TextField()

    def save(self, *args, **kwargs):
        # Si es un nuevo movimiento (no tiene PK aún)
        if not self.pk:
            self.recurso.cantidad_total += self.cantidad
            self.recurso.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Movimiento de {self.recurso.nombre}: {self.cantidad}"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.fecha})"
