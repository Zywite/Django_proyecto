
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Habitacion, Reserva, Recurso, Clima
from .forms import HabitacionForm

def index(request):
    num_habitaciones = Habitacion.objects.count()
    num_reservas = Reserva.objects.count()
    num_recursos = Recurso.objects.count()

    context = {
        'num_habitaciones': num_habitaciones,
        'num_reservas': num_reservas,
        'num_recursos': num_recursos,
    }

    return render(request, 'gestion/index.html', context)

class HabitacionListView(ListView):
    model = Habitacion
    template_name = 'gestion/habitacion_list.html'

class HabitacionCreateView(CreateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'gestion/habitacion_form.html'
    success_url = reverse_lazy('habitacion_list')

class HabitacionUpdateView(UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'gestion/habitacion_form.html'
    success_url = reverse_lazy('habitacion_list')

class HabitacionDeleteView(DeleteView):
    model = Habitacion
    template_name = 'gestion/habitacion_confirm_delete.html'
    success_url = reverse_lazy('habitacion_list')

class ReservaListView(ListView):
    model = Reserva
    template_name = 'gestion/reserva_list.html'

class RecursoListView(ListView):
    model = Recurso
    template_name = 'gestion/recurso_list.html'

class ClimaListView(ListView):
    model = Clima
    template_name = 'gestion/clima_list.html'
