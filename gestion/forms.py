from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Habitacion, Recurso, MovimientoRecurso, Clima, Usuario

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'

class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = '__all__'

class MovimientoRecursoForm(forms.ModelForm):
    class Meta:
        model = MovimientoRecurso
        fields = ['recurso', 'cantidad', 'motivo']

class ClimaForm(forms.ModelForm):
    class Meta:
        model = Clima
        fields = '__all__'

# Formularios de Autenticación
class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    apellido = forms.CharField(max_length=100, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'email', 'username', 'telefono', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases de Bootstrap a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
