from django import forms
from .models import Muestra
class MuestraForm(forms.ModelForm):
    class Meta:
        model = Muestra
        fields = '__all__'
