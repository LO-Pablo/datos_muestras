from django import forms
from .models import Muestra, Localizacion, Estudio, Envio
from itertools import product

class MuestraForm(forms.ModelForm):
    # Formulario basado en el modelo Muestra, se incluyen todos los campos del modelo
    class Meta:
        model = Muestra
        fields = '__all__'

class UploadExcel(forms.Form):
    # Formulario para subir un archivo Excel de las muestras
    excel_file = forms.FileField(required=False)
class LocalizacionForm(forms.Form):
    # Formulario basado en el modelo Localizacion, se incluyen todos los campos del modelo
    Congelador = forms.IntegerField(min_value=1)
    Estante = forms.IntegerField(min_value=1)
    Posicion_estante = forms.IntegerField(min_value=1)
    Rack= forms.IntegerField(min_value=1)
    Caja= forms.IntegerField(min_value=1)
    Posicion_caja = forms.IntegerField(min_value=1)
    Subposiciones = forms.IntegerField(min_value=1)
        #self.fields['muestra'].queryset = Muestra.objects.filter(localizacion__isnull=True)
        
    def save(self):
        if self.is_valid():
            congelador = self.cleaned_data.get('Congelador')
            estante = self.cleaned_data.get('Estante')
            rack = self.cleaned_data.get('Rack')
            caja = self.cleaned_data.get('Caja')
            subposiciones = self.cleaned_data.get('Subposiciones')
            for a,b,c,d,e in product(range(congelador),range(estante),range(rack),range(caja),range(subposiciones)):
                    Localizacion.objects.update_or_create(
                        congelador=a+1, estante=b+1, posicion_rack_estante=c+1,
                        rack=c+1, caja=d+1, posicion_caja_rack=d+1, subposicion=e+1
                    )

    
class LocalizacionForm_archivar(forms.ModelForm):
    # Formulario basado en el modelo Localizacion, se incluyen todos los campos del modelo
    class Meta:
        model = Localizacion
        fields = ['muestra']

    congelador = forms.CharField(max_length=50)
    estante = forms.CharField(max_length=50)
    posicion_rack_estante = forms.CharField(max_length=50)
    rack = forms.CharField(max_length=50)
    posicion_caja_rack = forms.CharField(max_length=50)
    caja = forms.CharField(max_length=50)
    subposicion = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data=super().clean()

        #Verificar que la muestra no esté ya archivada
        try:
            Localizacion.objects.get(muestra='muestra')
            raise forms.ValidationError("La muestra ya está archivada en una localización.")
        except Localizacion.DoesNotExist:
            pass
        
        
        # Verificar que la posición especificada esté vacía
        try:
            Localizacion.objects.get(
                congelador=cleaned_data.get("congelador"),
                estante=cleaned_data.get("estante"),
                posicion_rack_estante=cleaned_data.get("posicion_rack_estante"),
                rack=cleaned_data.get("rack"),
                posicion_caja_rack=cleaned_data.get("posicion_caja_rack"),
                caja=cleaned_data.get("caja"),
                subposicion=cleaned_data.get("subposicion"),
                muestra__isnull=True
            )
        except Localizacion.DoesNotExist:
            raise forms.ValidationError("La posición no existe o ya está ocupada.")
        return cleaned_data