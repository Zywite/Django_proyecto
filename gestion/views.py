
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Habitacion, Reserva, Recurso, Clima, MovimientoRecurso, Usuario
from .forms import HabitacionForm, RecursoForm, MovimientoRecursoForm, ClimaForm, RegistroForm, LoginForm

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

class RecursoCreateView(CreateView):
    model = Recurso
    form_class = RecursoForm
    template_name = 'gestion/recurso_form.html'
    success_url = reverse_lazy('recurso_list')

class RecursoUpdateView(UpdateView):
    model = Recurso
    form_class = RecursoForm
    template_name = 'gestion/recurso_form.html'
    success_url = reverse_lazy('recurso_list')

class RecursoDeleteView(DeleteView):
    model = Recurso
    template_name = 'gestion/recurso_confirm_delete.html'
    success_url = reverse_lazy('recurso_list')

class ClimaListView(ListView):
    model = Clima
    template_name = 'gestion/clima_list.html'

class ClimaCreateView(CreateView):
    model = Clima
    form_class = ClimaForm
    template_name = 'gestion/clima_form.html'
    success_url = reverse_lazy('clima_list')

class ClimaUpdateView(UpdateView):
    model = Clima
    form_class = ClimaForm
    template_name = 'gestion/clima_form.html'
    success_url = reverse_lazy('clima_list')

class ClimaDeleteView(DeleteView):
    model = Clima
    template_name = 'gestion/clima_confirm_delete.html'
    success_url = reverse_lazy('clima_list')

class MovimientoRecursoListView(ListView):
    model = MovimientoRecurso
    template_name = 'gestion/movimiento_recurso_list.html'

class MovimientoRecursoCreateView(CreateView):
    model = MovimientoRecurso
    form_class = MovimientoRecursoForm
    template_name = 'gestion/movimiento_recurso_form.html'
    success_url = reverse_lazy('movimiento_recurso_list')

class MovimientoRecursoUpdateView(UpdateView):
    model = MovimientoRecurso
    form_class = MovimientoRecursoForm
    template_name = 'gestion/movimiento_recurso_form.html'
    success_url = reverse_lazy('movimiento_recurso_list')


# ================ VISTAS DE AUTENTICACIÓN ================

class RegistroView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        # Después de registrarse, se redirige automáticamente a login
        return response


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Usar la función login de django para crear la sesión
            from django.contrib.auth import login as auth_login
            auth_login(request, user)
            return redirect('index')
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('login')
