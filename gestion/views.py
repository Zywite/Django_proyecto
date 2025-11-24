
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Habitacion, Reserva, Recurso, Clima, MovimientoRecurso, Usuario, Contacto
from .forms import HabitacionForm, RecursoForm, MovimientoRecursoForm, ClimaForm, RegistroForm, LoginForm, ContactoForm

@login_required
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

class HabitacionListView(LoginRequiredMixin, ListView):
    model = Habitacion
    template_name = 'gestion/habitacion_list.html'
    ordering = ['numero']

class HabitacionCreateView(LoginRequiredMixin, CreateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'gestion/habitacion_form.html'
    success_url = reverse_lazy('habitacion_list')

class HabitacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = 'gestion/habitacion_form.html'
    success_url = reverse_lazy('habitacion_list')

class HabitacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Habitacion
    template_name = 'gestion/habitacion_confirm_delete.html'
    success_url = reverse_lazy('habitacion_list')

class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'gestion/reserva_list.html'
    ordering = ['-fecha_inicio']

class RecursoListView(LoginRequiredMixin, ListView):
    model = Recurso
    template_name = 'gestion/recurso_list.html'
    ordering = ['nombre']

class RecursoCreateView(LoginRequiredMixin, CreateView):
    model = Recurso
    form_class = RecursoForm
    template_name = 'gestion/recurso_form.html'
    success_url = reverse_lazy('recurso_list')

class RecursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Recurso
    form_class = RecursoForm
    template_name = 'gestion/recurso_form.html'
    success_url = reverse_lazy('recurso_list')

class RecursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Recurso
    template_name = 'gestion/recurso_confirm_delete.html'
    success_url = reverse_lazy('recurso_list')

class ClimaListView(LoginRequiredMixin, ListView):
    model = Clima
    template_name = 'gestion/clima_list.html'
    ordering = ['-fecha']

class ClimaCreateView(LoginRequiredMixin, CreateView):
    model = Clima
    form_class = ClimaForm
    template_name = 'gestion/clima_form.html'
    success_url = reverse_lazy('clima_list')

class ClimaUpdateView(LoginRequiredMixin, UpdateView):
    model = Clima
    form_class = ClimaForm
    template_name = 'gestion/clima_form.html'
    success_url = reverse_lazy('clima_list')

class ClimaDeleteView(LoginRequiredMixin, DeleteView):
    model = Clima
    template_name = 'gestion/clima_confirm_delete.html'
    success_url = reverse_lazy('clima_list')

class MovimientoRecursoListView(LoginRequiredMixin, ListView):
    model = MovimientoRecurso
    template_name = 'gestion/movimiento_recurso_list.html'
    ordering = ['-fecha']

class MovimientoRecursoCreateView(LoginRequiredMixin, CreateView):
    model = MovimientoRecurso
    form_class = MovimientoRecursoForm
    template_name = 'gestion/movimiento_recurso_form.html'
    success_url = reverse_lazy('movimiento_recurso_list')

class MovimientoRecursoUpdateView(LoginRequiredMixin, UpdateView):
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

class ContactoCreateView(CreateView):
    model = Contacto
    form_class = ContactoForm
    template_name = 'gestion/contacto_form.html'
    success_url = reverse_lazy('contacto_success')

class ContactoSuccessView(TemplateView):
    template_name = 'gestion/contacto_success.html'
