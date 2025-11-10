from django.contrib import admin
from .models import (
    Usuario,
    Habitacion,
    Reserva,
    Clima,
    Recurso,
    MovimientoRecurso
)

admin.site.register(Usuario)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Clima)
admin.site.register(Recurso)
admin.site.register(MovimientoRecurso)