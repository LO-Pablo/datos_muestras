from django import forms
from .models import Muestra

class MuestraForm(forms.ModelForm):
    # Formulario basado en el modelo Muestra, se incluyen todos los campos del modelo
    class Meta:
        model = Muestra
        fields = '__all__'
