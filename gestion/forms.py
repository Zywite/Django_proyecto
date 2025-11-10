from django import forms
from .models import Habitacion, Recurso, MovimientoRecurso, Clima

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
