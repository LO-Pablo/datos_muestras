from django.http import HttpResponse
from .models import Muestra, Localizacion, Estudio, Envio
from django.template import loader
from .forms import MuestraForm, LocalizacionForm, LocalizacionForm_archivar, UploadExcel
from django.db import transaction
from django.contrib import messages  
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import pandas as pd

def principal(request):
    # Vista principal de la aplicación, muestra una página de bienvenida
    template = loader.get_template('principal.html')
    return HttpResponse(template.render(request=request))
@login_required

# Vistas para Muestras

def muestras_todas(request):
    # Vista que muestra todas las muestras, requiere que el usuario esté autenticado
    muestras = Muestra.objects.prefetch_related('localizacion')
    # Filtrado de muestras si se proporcionan parámetros de búsqueda
    field_names = [f.name for f in Muestra._meta.local_fields if f.name not in ('id')]
    for field in field_names:
        if request.GET.get(field):
            filter_kwargs = {f"{field}__icontains": request.GET[field]}
            muestras = muestras.filter(**filter_kwargs)
    # Eliminación de muestras seleccionadas en la tabla 
    for muestra in muestras:    
        if request.GET.get(f'{muestra.id}'):
            eliminar_muestra(request, muestra.id_individuo, muestra.nom_lab)
    template = loader.get_template('muestras_todas.html')
    context = {    
        'muestras': muestras,
        'field_names': field_names
    }
    return HttpResponse(template.render(context, request))
@login_required
@permission_required('muestras.can_view_muestras_web')
def detalles_muestra(request, id_individuo, nom_lab):
    # Vista que muestra los detalles de una muestra específica, requiere permiso para ver muestras
    muestra = Muestra.objects.get(id_individuo=id_individuo, nom_lab=nom_lab)
    template = loader.get_template('detalles_muestra.html')
    context = {
        'muestra': muestra,
    }
    return HttpResponse(template.render(context, request))
@permission_required('muestras.can_add_muestras_web')
def nueva_muestra(request):
    # Vista para crear una nueva muestra, requiere permiso para añadir muestras
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_muestra', id_individuo=form.instance.id_individuo, nom_lab=form.instance.nom_lab)
    else:
        form = MuestraForm()
    return render(request, 'nueva_muestra.html', {'form': form})
@permission_required('muestras.can_add_muestras_web')
def upload_excel(request):
    if request.method=="POST":
        form = UploadExcel(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            rename_columns = {
                'ID Individuo': 'id_individuo', 
                'Nombre Laboratorio': 'nom_lab',
                'ID Material': 'id_material',
                'Volumen Actual': 'volumen_actual',
                'Unidad Volumen': 'unidad_volumen',
                'Concentracion Actual': 'concentracion_actual',
                'Unidad Concentracion': 'unidad_concentracion',
                'Masa Actual': 'masa_actual',
                'Unidad Masa': 'unidad_masa',
                'Fecha Extraccion': 'fecha_extraccion',
                'Fecha Llegada': 'fecha_llegada',
                'Observaciones': 'observaciones',
                'Estado Inicial': 'estado_inicial',
                'Centro Procedencia': 'centro_procedencia',
                'Lugar Procedencia': 'lugar_procedencia'
            }
            df.rename(columns=rename_columns, inplace=True)
            for _, row in df.iterrows():
                muestra, created = Muestra.objects.update_or_create(
                    id_individuo=row['id_individuo'],
                    nom_lab=row['nom_lab'],
                    id_material=row['id_material'],
                    volumen_actual=row['volumen_actual'],
                    unidad_volumen=row['unidad_volumen'],
                    concentracion_actual=row['concentracion_actual'],
                    unidad_concentracion=row['unidad_concentracion'],
                    masa_actual=row['masa_actual'],
                    unidad_masa=row['unidad_masa'],
                    fecha_extraccion=row['fecha_extraccion'],
                    fecha_llegada = row['fecha_llegada'],
                    observaciones= row['observaciones'],
                    estado_inicial=row['estado_inicial'],
                    centro_procedencia=row['centro_procedencia'],
                    lugar_procedencia=row['lugar_procedencia'],
                )
                if not created:
                    messages.info(request, f'Muestra {muestra.nom_lab} ya existe, el excel no se ha procesado correctamente')
            if created:
                messages.success(request, 'Archivo excel procesado correctamente.')
            return redirect('upload_excel')
    else:
        form = UploadExcel()
    return render(request, 'upload_excel.html', {'form': form}) 
@permission_required('muestras.can_change_muestras_web')
def editar_muestra(request, id_individuo, nom_lab):
    # Vista para editar una muestra existente, requiere permiso para cambiar muestras
    muestra = Muestra.objects.get(id_individuo=id_individuo, nom_lab=nom_lab)
    if request.method == 'POST':
        form = MuestraForm(request.POST, instance=muestra)
        if form.is_valid():
            form.save()
            return redirect('detalles_muestra', id_individuo=form.instance.id_individuo, nom_lab=form.instance.nom_lab)
    else:
        form = MuestraForm(instance=muestra)
    return render(request, 'editar_muestra.html', {'form': form, 'muestra': muestra})
@permission_required('muestras.can_delete_muestras_web')
def eliminar_muestra(request, id_individuo, nom_lab):
    # Vista para eliminar una muestra, requiere permiso para eliminar muestras
    muestra = get_object_or_404(Muestra,id_individuo=id_individuo, nom_lab=nom_lab)
    muestra.delete()
    return redirect('muestras_todas')

# Vistas para Localizacion

def localizaciones(request):
    # Vista que muestra todas las localizaciones, tengan o no muestra
    localizaciones = Localizacion.objects.all().values().distinct()
    template = loader.get_template('localizaciones_todas.html')
    context = {
        'localizaciones': localizaciones,
    }
    return HttpResponse(template.render(context, request))

def nueva_localizacion(request):
    # Vista para crear una nueva localizacion, con muestra o no
    if request.method == 'POST':
        form = LocalizacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('localizaciones_todas')
    else:
        form = LocalizacionForm()   
    return render(request, 'localizaciones_nueva.html', {'form': form})

@transaction.atomic
def archivar_muestra(request):
    # Vista para archivar una muestra en una localización específica que esté vacía 
    if request.method == 'POST':
        form = LocalizacionForm_archivar(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            try:
                muestra_obj = data['muestra']
                slot = Localizacion.objects.select_for_update().get(
                    congelador=data['congelador'],
                    estante=data['estante'],
                    posicion_rack_estante=data['posicion_rack_estante'],
                    rack=data['rack'],
                    posicion_caja_rack=data['posicion_caja_rack'],
                    caja=data['caja'],
                    subposicion=data['subposicion'],
                    muestra__isnull=True 
                )
                
            
                slot.muestra = muestra_obj
                slot.save()
                
        
                return redirect('localizaciones_todas') 
                
            except Muestra.DoesNotExist:
                
                messages.error(request, "Error interno: La muestra no fue encontrada.")
            
            except Localizacion.DoesNotExist:
                 
                messages.error(request, "Error interno: La ubicación ya no está disponible o no existe.")
                
    else:
        form =  LocalizacionForm_archivar()
        
    context = {'form': form}
    return render(request, 'archivar_muestra.html', context)