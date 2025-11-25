from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    Habitacion,
    Recurso,
    MovimientoRecurso,
    Clima,
    Usuario,
    Contacto,
    Reserva,
)


class HabitacionForm(forms.ModelForm):
    """
    Formulario para la creación y edición de habitaciones.
    """

    class Meta:
        model = Habitacion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class RecursoForm(forms.ModelForm):
    """
    Formulario para la gestión de recursos.
    """

    class Meta:
        model = Recurso
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class MovimientoRecursoForm(forms.ModelForm):
    """
    Formulario para registrar movimientos de stock.
    """

    class Meta:
        model = MovimientoRecurso
        fields = ["recurso", "cantidad", "motivo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ClimaForm(forms.ModelForm):
    class Meta:
        model = Clima
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class RegistroForm(UserCreationForm):
    """
    Formulario extendido de creación de usuarios con campos adicionales.
    """

    nombre = forms.CharField(max_length=100, required=True, label="Nombre")
    apellido = forms.CharField(max_length=100, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Email")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")

    class Meta:
        model = Usuario
        fields = (
            "nombre",
            "apellido",
            "email",
            "username",
            "telefono",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = "cliente"  # Asignar rol de cliente por defecto
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "email", "mensaje"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ReservaClienteForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin"]
        widgets = {
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "fecha_fin": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }
