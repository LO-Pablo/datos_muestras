from django import forms
from .models import Muestra, Localizacion, Estudio, Envio

class MuestraForm(forms.ModelForm):
    # Formulario basado en el modelo Muestra, se incluyen todos los campos del modelo
    class Meta:
        model = Muestra
        fields = '__all__'
class LocalizacionForm(forms.ModelForm):
    # Formulario basado en el modelo Localizacion, se incluyen todos los campos del modelo
    class Meta:
        model = Localizacion
        fields = '__all__'