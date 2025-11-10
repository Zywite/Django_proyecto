
from django.urls import path
from .views import (
    index,
    HabitacionListView,
    HabitacionCreateView,
    HabitacionUpdateView,
    HabitacionDeleteView,
    ReservaListView,
    RecursoListView,
    ClimaListView,
)

urlpatterns = [
    path('', index, name='index'),
    path('habitaciones/', HabitacionListView.as_view(), name='habitacion_list'),
    path('habitaciones/crear/', HabitacionCreateView.as_view(), name='habitacion_crear'),
    path('habitaciones/<int:pk>/editar/', HabitacionUpdateView.as_view(), name='habitacion_editar'),
    path('habitaciones/<int:pk>/eliminar/', HabitacionDeleteView.as_view(), name='habitacion_eliminar'),
    path('reservas/', ReservaListView.as_view(), name='reserva_list'),
    path('recursos/', RecursoListView.as_view(), name='recurso_list'),
    path('clima/', ClimaListView.as_view(), name='clima_list'),
]
