from django import forms
from .models import Muestra, Localizacion, Estudio, Envio, Documento
from itertools import product

class MuestraForm(forms.ModelForm):
    # Formulario basado en el modelo Muestra, se incluyen todos los campos del modelo
    class Meta:
        model = Muestra
        fields = '__all__'

class UploadExcel(forms.Form):
    # Formulario para subir un archivo Excel 
    excel_file = forms.FileField(required=False)
class LocalizacionForm(forms.Form):
    """Bulk creator: crea varias Localizacion a la vez.

    Campos (enteros) indican cuántas posiciones crear en cada dimensión.
    Para cada dimensión hay un campo is_bulk_X que determina si el número X
    significa "crear posiciones 1..X" (bulk=True) o "crear solo posición X" (bulk=False).
    """

    Congeladores = forms.IntegerField(min_value=1, initial=1, help_text="Número de congeladores")
    is_bulk_congeladores = forms.BooleanField(required=False, initial=True, label="Crear congeladores 1 a N")

    Estantes = forms.IntegerField(min_value=1, initial=1, help_text="Número de estantes por congelador")
    is_bulk_estantes = forms.BooleanField(required=False, initial=True, label="Crear estantes 1 a N")

    Posiciones_de_los_racks_en_el_estante = forms.IntegerField(min_value=1, initial=1, help_text="Número de posiciones de rack por estante")
    is_bulk_posiciones_de_los_racks_en_el_estante = forms.BooleanField(required=False, initial=True, label="Crear posiciones 1 a N")

    Racks = forms.IntegerField(min_value=1, initial=1, help_text="Número de racks por posición de estante")
    is_bulk_racks = forms.BooleanField(required=False, initial=True, label="Crear racks 1 a N")

    Posiciones_de_la_cajas_en_los_racks = forms.IntegerField(min_value=1, initial=1, help_text="Número de posiciones de caja por rack")
    is_bulk_posiciones_de_la_cajas_en_los_racks = forms.BooleanField(required=False, initial=True, label="Crear posiciones 1 a N")

    Cajas = forms.IntegerField(min_value=1, initial=1, help_text="Número de cajas por posición de caja en el rack")
    is_bulk_cajas = forms.BooleanField(required=False, initial=True, label="Crear cajas 1 a N")

    Subposiciones = forms.IntegerField(min_value=1, initial=1, help_text="Número de subposiciones por caja")
    is_bulk_subposiciones = forms.BooleanField(required=False, initial=True, label="Crear subposiciones 1 a N")

    def save(self):
        """Crear las localizaciones según los valores y modos (bulk/single) especificados."""
        if not self.is_valid():
            raise ValueError("Formulario no válido")

        # Obtener valores y modos para cada dimensión
        dims = {
            'congelador': (self.cleaned_data['Congeladores'], self.cleaned_data['is_bulk_congeladores']),
            'estante': (self.cleaned_data['Estantes'], self.cleaned_data['is_bulk_estantes']),
            'posicion_rack_estante': (self.cleaned_data['Posiciones_de_los_racks_en_el_estante'], self.cleaned_data['is_bulk_posiciones_de_los_racks_en_el_estante']),
            'rack': (self.cleaned_data['Racks'], self.cleaned_data['is_bulk_racks']),
            'posicion_caja_rack': (self.cleaned_data['Posiciones_de_la_cajas_en_los_racks'], self.cleaned_data['is_bulk_posiciones_de_la_cajas_en_los_racks']),
            'caja': (self.cleaned_data['Cajas'], self.cleaned_data['is_bulk_cajas']),
            'subposicion': (self.cleaned_data['Subposiciones'], self.cleaned_data['is_bulk_subposiciones'])
        }

        # Convertir cada dimensión a su rango de valores según el modo
        ranges = {}
        for dim, (value, is_bulk) in dims.items():
            if is_bulk:
                # Modo bulk: generar posiciones 1 a N
                ranges[dim] = range(1, value + 1)
            else:
                # Modo single: usar solo el valor N
                ranges[dim] = [value]

        # Crear todas las combinaciones válidas
        created = 0
        for cong, est, pos_rack, rack, pos_caja, caja, sub in product(
            ranges['congelador'],
            ranges['estante'],
            ranges['posicion_rack_estante'],
            ranges['rack'],
            ranges['posicion_caja_rack'],
            ranges['caja'],
            ranges['subposicion']
        ):
            # Convertir números a strings como espera el modelo
            loc_data = {
                'congelador': str(cong),
                'estante': str(est),
                'posicion_rack_estante': str(pos_rack),
                'rack': str(rack),
                'posicion_caja_rack': str(pos_caja),
                'caja': str(caja),
                'subposicion': str(sub),
            }
            # Crear o actualizar la localización
            obj, was_created = Localizacion.objects.update_or_create(
                **loc_data,  # usamos los mismos campos como lookup
                defaults={'muestra': None}  # siempre vacía al crear
            )
            created += 1

        return created
class archivar_muestra_form(forms.ModelForm):
        """Archivar una muestra en una localización específica."""
        class Meta:
            model = Localizacion
            fields = ['muestra', 'congelador', 'estante', 'posicion_rack_estante', 'rack', 'posicion_caja_rack', 'caja', 'subposicion']

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento 
        fields = '__all__'
