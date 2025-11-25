from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .mixins import AdminRequiredMixin
from .models import (
    Habitacion,
    Reserva,
    Recurso,
    Clima,
    MovimientoRecurso,
    Usuario,
    Contacto,
)
from .forms import (
    HabitacionForm,
    RecursoForm,
    MovimientoRecursoForm,
    ClimaForm,
    RegistroForm,
    LoginForm,
    ContactoForm,
    ReservaClienteForm,
)
from django.shortcuts import get_object_or_404


@login_required
def index(request):
    """
    Vista principal del dashboard.
    Muestra contadores generales de habitaciones, reservas y recursos.
    """
    num_habitaciones = Habitacion.objects.count()
    num_reservas = Reserva.objects.count()
    num_recursos = Recurso.objects.count()

    context = {
        "num_habitaciones": num_habitaciones,
        "num_reservas": num_reservas,
        "num_recursos": num_recursos,
    }

    return render(request, "gestion/index.html", context)


class HabitacionListView(LoginRequiredMixin, ListView):
    """
    Lista todas las habitaciones registradas.
    """

    model = Habitacion
    template_name = "gestion/habitacion_list.html"
    ordering = ["numero"]


class HabitacionCreateView(AdminRequiredMixin, CreateView):
    """
    Permite registrar una nueva habitación.
    """

    model = Habitacion
    form_class = HabitacionForm
    template_name = "gestion/habitacion_form.html"
    success_url = reverse_lazy("habitacion_list")


class HabitacionUpdateView(AdminRequiredMixin, UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = "gestion/habitacion_form.html"
    success_url = reverse_lazy("habitacion_list")


class HabitacionDeleteView(AdminRequiredMixin, DeleteView):
    model = Habitacion
    template_name = "gestion/habitacion_confirm_delete.html"
    success_url = reverse_lazy("habitacion_list")


class ReservaListView(LoginRequiredMixin, ListView):
    """
    Lista todas las reservas, ordenadas por fecha de inicio descendente.
    """

    model = Reserva
    template_name = "gestion/reserva_list.html"
    ordering = ["-fecha_inicio"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol != "administrador":
            queryset = queryset.filter(usuario=self.request.user)
        return queryset


class ReservaClienteCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaClienteForm
    template_name = "gestion/reserva_form.html"
    success_url = reverse_lazy("reserva_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        habitacion_id = self.kwargs.get("habitacion_id")
        form.instance.habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
        form.instance.estado = "pendiente"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habitacion_id = self.kwargs.get("habitacion_id")
        context["habitacion"] = get_object_or_404(Habitacion, pk=habitacion_id)
        return context


class RecursoListView(AdminRequiredMixin, ListView):
    model = Recurso
    template_name = "gestion/recurso_list.html"
    ordering = ["nombre"]


class RecursoCreateView(AdminRequiredMixin, CreateView):
    model = Recurso
    form_class = RecursoForm
    template_name = "gestion/recurso_form.html"
    success_url = reverse_lazy("recurso_list")


class RecursoUpdateView(AdminRequiredMixin, UpdateView):
    model = Recurso
    form_class = RecursoForm
    template_name = "gestion/recurso_form.html"
    success_url = reverse_lazy("recurso_list")


class RecursoDeleteView(AdminRequiredMixin, DeleteView):
    model = Recurso
    template_name = "gestion/recurso_confirm_delete.html"
    success_url = reverse_lazy("recurso_list")


class ClimaListView(LoginRequiredMixin, ListView):
    model = Clima
    template_name = "gestion/clima_list.html"
    ordering = ["-fecha"]


class ClimaCreateView(AdminRequiredMixin, CreateView):
    model = Clima
    form_class = ClimaForm
    template_name = "gestion/clima_form.html"
    success_url = reverse_lazy("clima_list")


class ClimaUpdateView(AdminRequiredMixin, UpdateView):
    model = Clima
    form_class = ClimaForm
    template_name = "gestion/clima_form.html"
    success_url = reverse_lazy("clima_list")


class ClimaDeleteView(AdminRequiredMixin, DeleteView):
    model = Clima
    template_name = "gestion/clima_confirm_delete.html"
    success_url = reverse_lazy("clima_list")


class MovimientoRecursoListView(AdminRequiredMixin, ListView):
    model = MovimientoRecurso
    template_name = "gestion/movimiento_recurso_list.html"
    ordering = ["-fecha"]


class MovimientoRecursoCreateView(AdminRequiredMixin, CreateView):
    model = MovimientoRecurso
    form_class = MovimientoRecursoForm
    template_name = "gestion/movimiento_recurso_form.html"
    success_url = reverse_lazy("movimiento_recurso_list")


class MovimientoRecursoUpdateView(AdminRequiredMixin, UpdateView):
    model = MovimientoRecurso
    form_class = MovimientoRecursoForm
    template_name = "gestion/movimiento_recurso_form.html"
    success_url = reverse_lazy("movimiento_recurso_list")


class RegistroView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    """

    model = Usuario
    form_class = RegistroForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()

        return response


class LoginView(View):
    """
    Vista personalizada para el inicio de sesión.
    """

    def get(self, request):
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            from django.contrib.auth import login as auth_login

            auth_login(request, user)
            return redirect("index")
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    from django.contrib.auth import logout as auth_logout

    auth_logout(request)
    return redirect("login")


class ContactoCreateView(CreateView):
    model = Contacto
    form_class = ContactoForm
    template_name = "gestion/contacto_form.html"
    success_url = reverse_lazy("contacto_success")


class ContactoSuccessView(TemplateView):
    template_name = "gestion/contacto_success.html"
