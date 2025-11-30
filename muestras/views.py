from django.http import HttpResponse, FileResponse
from .models import Muestra, Localizacion, Estudio, Envio, Documento, historial_estudios, historial_localizaciones,agenda_envio, registro_destruido
from django.template import loader
from .forms import MuestraForm, LocalizacionForm, UploadExcel, archivar_muestra_form, DocumentoForm, EstudioForm, Centroform
from django.db import transaction
from django.contrib import messages  
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
import pandas as pd
import io,base64
from reportlab.pdfgen import canvas
from django.conf import settings
import openpyxl,os
from django.db.models import Q
from django.db import IntegrityError, ProgrammingError
from django.utils import timezone 
from django.contrib.auth.models import User
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
    field_names = [f.name for f in Muestra._meta.local_fields if f.name not in ('id','estudio')]
    fields_loc = [f.name for f in Localizacion._meta.local_fields if f.name not in ('id','muestra')]
    if request.user.groups.filter(name='Investigadores'):
        muestras = Muestra.objects.filter(Q(estudio__investigador_principal__username=request.user.username) | Q(estudio = None))
    for field in field_names:
        if request.GET.get(field):
            filter_kwargs = {f"{field}__icontains": request.GET[field]}
            muestras = muestras.filter(**filter_kwargs)
    if request.GET.get('estudio'):
        filtro_estudio = request.GET['estudio']
        muestras = muestras.filter(estudio__nombre_estudio__icontains=filtro_estudio)

    '''
    # Crear un PDF con las muestras filtradas
    if request.GET.get('crear_pdf'):    
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        y = 800
        p.setFont("Helvetica", 16)
        p.drawString(30,y, "Listado de Muestras")
        p.setFont("Helvetica", 12)
        y -= 30
        p.drawString(30, y, "ID Individuo")
        p.drawString(150, y, "Nombre Laboratorio")
        p.drawString(300, y, "Localización")
        y-= 30
        for muestra in muestras:
            p.drawString(30, y, muestra.id_individuo)
            p.drawString(150, y, muestra.nom_lab)
            p.drawString(300, y, str(muestra.localizacion.first()) if muestra.localizacion.exists() else 'No archivada')
            y -= 20
            if y < 50:
                p.showPage()
                y = 800
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='listado_muestras.pdf')
    '''
     # Crear un Excel con las muestras filtradas 
    if request.GET.get('exportar_excel'):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="listado_muestras.xlsx"'
        wb = openpyxl.load_workbook(os.path.join(settings.BASE_DIR, 'datos_prueba', 'globalstaticfiles', 'listado_muestras.xlsx'))
        ws = wb.active
        row_num = 2
        for muestra in muestras:
            col_num = 1
            
            for field in field_names:
                value = muestra.__dict__[field]
                if value is None:
                    value = ''
                ws.cell(row_num, col_num).value= str(value)
                col_num += 1
            value = muestra.estudio.nombre_estudio if muestra.estudio else ''
            ws.cell(row_num, col_num).value= str(value)
            col_num += 1
            try:
                loc = Localizacion.objects.get(muestra=muestra.nom_lab)
                for field in fields_loc:
                    value = loc.__dict__[field]
                    if value is None:
                        value = ''
                    ws.cell(row_num, col_num).value= str(value)
                    col_num += 1
                row_num += 1
            except:
                row_num += 1
        wb.save(response)
        return response
    template = loader.get_template('muestras_todas.html')
    context = {    
        'muestras': muestras,
        'field_names': field_names
    }
    return HttpResponse(template.render(context, request))
@login_required
@permission_required('muestras.can_view_muestras_web')
def acciones_post(request):
    if request.method=="POST":
        muestras_seleccionadas = request.POST.getlist('muestra_id')
        if 'estudio' in request.POST:
            if muestras_seleccionadas:
                request.session['muestras_estudio']=muestras_seleccionadas
                return redirect('seleccionar_estudio')
        elif 'eliminar' in request.POST:
            if muestras_seleccionadas:
                muestras_a_procesar = Muestra.objects.filter(id__in=muestras_seleccionadas)
                for muestra in muestras_a_procesar:
                    eliminar_muestra(request, muestra.id_individuo, muestra.nom_lab) 
        elif 'envio' in request.POST:
            if muestras_seleccionadas:
                if 'muestras_envio' in request.session:
                    del request.session['muestras_envio']
                for muestra in muestras_seleccionadas:
                    if Muestra.objects.get(id=muestra).estado_actual == 'Destruida':
                        muestras_seleccionadas.remove(muestra)
                request.session['muestras_envio']=muestras_seleccionadas
                return redirect('agenda')
        elif 'destruir' in request.POST:
            if muestras_seleccionadas:
                muestras_a_destruir = Muestra.objects.filter(id__in=muestras_seleccionadas)
                for sample in muestras_a_destruir:
                    sample.estado_actual = 'Destruida'
                    sample.volumen_actual = 0
                    sample.concentracion_actual = 0
                    sample.save()
                    if Localizacion.objects.filter(muestra=sample).exists():
                        loc = Localizacion.objects.get(muestra=sample)
                        loc.muestra = None
                        loc.save()
                    registro_destruccion = registro_destruido.objects.create(muestra = sample,
                                                                             fecha = timezone.now(),
                                                                             usuario = request.user)
                    registro_destruccion.save()
                    
    return redirect('muestras_todas')    
def detalles_muestra(request, nom_lab):
    # Vista que muestra los detalles de una muestra específica, requiere permiso para ver muestras
    muestra = Muestra.objects.get(nom_lab=nom_lab)
    template = loader.get_template('detalles_muestra.html')
    context = {
        'muestra': muestra,
    }
    return HttpResponse(template.render(context, request))
@permission_required('muestras.can_add_muestras_web')


def añadir_muestras(request):
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('muestras_todas')
    else:
        form = MuestraForm()
    return render(request, 'añadir_muestras.html', {'form': form})
"""
    MuestraFormset = formset_factory(MuestraForm)
    formset= MuestraFormset()
    if request.method == 'POST':
        formset = MuestraFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
    else:
        formset = MuestraFormset()
    return render(request, 'añadir_muestras.html', {'formset': formset})
"""

@permission_required('muestras.can_delete_muestras_web')
def eliminar_muestra(request, id_individuo, nom_lab):
    # Vista para eliminar una muestra, requiere permiso para eliminar muestras
    muestra = get_object_or_404(Muestra,id_individuo=id_individuo, nom_lab=nom_lab)
    muestra.delete()
    return redirect('muestras_todas')
@permission_required('muestras.can_add_muestras_web')
def upload_excel(request):
    if request.method=="POST":
        form = UploadExcel(request.POST, request.FILES)
        if 'confirmar' in request.POST:
            messages.success(request, 'Las muestras se han añadido correctamente.')
            ids_to_delete = request.session.pop('ids_error_muestras', [])
            Muestra.objects.filter(nom_lab__in=ids_to_delete).delete()
        elif 'cancelar' in request.POST:
            # Eliminación de las muestras y localizaciones añadidas del excel
            ids_to_delete = request.session.pop('nuevos_ids', [])
            Muestra.objects.filter(id__in=ids_to_delete).delete()
        elif 'excel_file' in request.FILES:
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                excel_bytes = excel_file.read()
                request.session['excel_file_name'] = excel_file.name
                request.session['excel_file_base64']= base64.b64encode(excel_bytes).decode()
                excel_stream = io.BytesIO(excel_bytes)
                df = pd.read_excel(excel_stream)
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
                    'Lugar Procedencia': 'lugar_procedencia',
                    'Estado actual': 'estado_actual',
                    'Congelador': 'congelador', 
                    'Estante': 'estante',
                    'Posición del rack en el estante': 'posicion_rack_estante',
                    'Rack': 'rack',
                    'Posición de la caja en el rack': 'posicion_caja_rack',
                    'Caja': 'caja',
                    'Subposición': 'subposicion',
                    'Estudio':'estudio'
                    
                }
                df.rename(columns=rename_columns, inplace=True)
                errors = 0
                errors_loc = 0
                errores_estudio = 0
                campos_vacios = 0
                localizaciones_ocupadas = 0
                nuevos_ids = []
                nuevos_ids_loc = []
                ids_error_muestras = []
                ids_error_localizaciones = []
                ids_formato_incorrecto = []
                ids_campos_vacios =[]
                ids_localizaciones_ocupadas = []
                columna_errores_formato = []
                numero_registros = 0
                for _, row in df.iterrows():
                    def normalize_value(value):
                        if pd.isna(value) or value is None:
                             return None
                        return value
                    numero_registros += 1
                    for campo in ['volumen_actual', 'concentracion_actual', 'masa_actual']:
                        try:
                            float(row[campo])
                        except:
                            columna_errores_formato.append(df.columns.get_loc(campo))
                    for campo in ['fecha_extraccion', 'fecha_llegada']:
                        try:
                            pd.to_datetime(row[campo], errors='raise')
                        except:
                            columna_errores_formato.append(df.columns.get_loc(campo)) 

                    nombre_estudio_excel = row['estudio']
                    if pd.isna(nombre_estudio_excel):
                        estudio_instance = None
                    else:
                        try:
                            estudio_instance = Estudio.objects.get(nombre_estudio=nombre_estudio_excel)
                        except  Exception:
                            estudio_instance = None
                            errores_estudio += 1
                    muestra, created = Muestra.objects.update_or_create(
                        id_individuo=row['id_individuo'],
                        nom_lab=row['nom_lab'],
                        id_material=normalize_value(row['id_material']),
                        volumen_actual=normalize_value(row['volumen_actual']),
                        unidad_volumen=normalize_value(row['unidad_volumen']),
                        concentracion_actual=normalize_value(row['concentracion_actual']),
                        unidad_concentracion=normalize_value(row['unidad_concentracion']),
                        masa_actual=normalize_value(row['masa_actual']),
                        unidad_masa=normalize_value(row['unidad_masa']),
                        fecha_extraccion=normalize_value(row['fecha_extraccion']),
                        fecha_llegada = normalize_value(row['fecha_llegada']),
                        observaciones= normalize_value(row['observaciones']),
                        estado_inicial=normalize_value(row['estado_inicial']),
                        centro_procedencia=normalize_value(row['centro_procedencia']),
                        lugar_procedencia=normalize_value(row['lugar_procedencia']),
                        estado_actual=normalize_value(row['estado_actual']),
                        estudio = estudio_instance
                        )
                    if estudio_instance != None:
                        historial_estudio = historial_estudios.objects.create(muestra=muestra, estudio=estudio_instance,
                                                                        fecha_asignacion=timezone.now(), usuario_asignacion=request.user)
                    
                        historial_estudio.save()
                    def normalize_charfield_value(value):
                        if pd.isna(value) or value is None:
                            return None
                        try:
                            if isinstance(value, (float, int)) and value == int(value):
                                return str(int(value))

                        except ValueError:
                            return str(value).strip()
                    localizacion, loc_created = Localizacion.objects.update_or_create(
                        muestra = muestra,
                        congelador=normalize_charfield_value(row['congelador']),
                        estante=normalize_charfield_value(row['estante']), 
                        posicion_rack_estante=normalize_charfield_value(row['posicion_rack_estante']),
                        rack=normalize_charfield_value(row['rack']),
                        posicion_caja_rack=normalize_charfield_value(row['posicion_caja_rack']),
                        caja=normalize_charfield_value(row['caja']),
                        subposicion=normalize_value(row['subposicion'])    
                    )
                    if created:
                        nuevos_ids.append(muestra.id)
                    if loc_created:
                        nuevos_ids_loc.append(localizacion.id)
                        Localizacion.objects.filter(congelador = localizacion.congelador, 
                                                        estante = localizacion.estante,
                                                        posicion_rack_estante = localizacion.posicion_rack_estante,
                                                        rack = localizacion.rack,
                                                        posicion_caja_rack = localizacion.posicion_caja_rack,
                                                        caja = localizacion.caja,
                                                        subposicion = localizacion.subposicion,
                                                        muestra__isnull=True).delete()
                        historial_loc = historial_localizaciones.objects.create(muestra=muestra, localizacion=localizacion,
                                                                    fecha_asignacion=timezone.now(), usuario_asignacion=request.user)
                
                        historial_loc.save()
                    
                    elif not created:
                        ids_error_muestras.append(muestra.nom_lab)
                        errors+=1
                    elif not loc_created:
                        errors_loc+=1
                        ids_error_localizaciones.append(muestra.nom_lab)
                    redirect('upload_excel')
                    
                    for column in df.columns:
                        if pd.isna(row[column]):
                            if column in [f.name for f in Muestra._meta.local_fields if f.name in ('nom_lab','id_individuo')] or column in [f.name for f in Localizacion._meta.local_fields]:
                                if column =='nom_lab':
                                    ids_error_muestras.append(None)
                                    errors+=1
                                elif column =='id_individuo':
                                    ids_error_muestras.append(row["nom_lab"])
                                    errors += 1
                                    Muestra.objects.filter(id=nuevos_ids[len(nuevos_ids)-1]).delete()
                                else:
                                    ids_error_muestras.append(row["nom_lab"])
                                    errors_loc+=1
                                    if not pd.isna(row['nom_lab']):
                                        Muestra.objects.filter(id=nuevos_ids[len(nuevos_ids)-1]).delete()
                                        if not localizacion.id == None:
                                            localizacion.delete()
                            elif column in [f.name for f in Muestra._meta.local_fields if f.name not in ('nom_lab','id_individuo')]:
                                Muestra.objects.filter(nom_lab=row['nom_lab']).update(**{column : None})
                                ids_campos_vacios.append(row['nom_lab']) 
                                campos_vacios += 1
                    if Localizacion.objects.filter(
                        ~Q(muestra__nom_lab=row['nom_lab']) | Q(muestra__isnull=True),
                        congelador=row['congelador'],
                        estante=row['estante'], 
                        posicion_rack_estante=row['posicion_rack_estante'],
                        rack=row['rack'],
                        posicion_caja_rack=row['posicion_caja_rack'],
                        caja=row['caja'],
                        subposicion=normalize_value(row['subposicion'])
                    ):
                        ids_localizaciones_ocupadas.append(row['nom_lab'])
                        localizaciones_ocupadas += 1
                request.session['nuevos_ids'] = nuevos_ids
                request.session['nuevos_ids_loc'] = nuevos_ids_loc
                request.session['ids_error_muestras'] = ids_error_muestras
                request.session['ids_error_localizaciones'] = ids_error_localizaciones
                request.session['ids_formato_incorrecto'] = ids_formato_incorrecto
                request.session['ids_campos_vacios'] = ids_campos_vacios
                request.session['ids_localizaciones_ocupadas'] = ids_localizaciones_ocupadas
                request.session['columna_errores_formato'] = columna_errores_formato
                messages.info(request, f'El excel subido tiene {numero_registros} registros.')
                if errors==0 and errors_loc==0:
                    messages.success(request, 'Y no tiene errores en ningún campo.')
                    if campos_vacios!=0:
                        messages.info(request,f"Aunque tiene {campos_vacios} campos vacios en algunas muestras.")
                    elif localizaciones_ocupadas!=0:
                        messages.info(request,f"Aunque hay {localizaciones_ocupadas} muestras que se están intentando archivar en una posición ocupada por otra muestra.")
                else:
                    messages.warning(request, f'Y contiene {errors} errores de los campos de las muestras, {errores_estudio} errores en el campo de estudios y {errors_loc} de los campos de localización.')
                return render(request, 'confirmacion_upload.html')
        elif 'excel_errores' in request.POST:
                    ids_error_muestras = request.session.get('ids_error_muestras', [])
                    ids_error_localizaciones = request.session.get('ids_error_localizaciones', [])
                    ids_formato_incorrecto = request.session.get('ids_formato_incorrecto', [])
                    ids_campos_vacios=request.session.get('ids_campos_vacios', [])
                    ids_localizaciones_ocupadas=request.session.get('ids_localizaciones_ocupadas', [])
                    columna_errores_formato = request.session.get('columna_errores_formato',[])
                    excel_bytes = base64.b64decode(request.session.get('excel_file_base64'))
                    excel_file = io.BytesIO(excel_bytes)
                    wb = openpyxl.load_workbook(excel_file)
                    ws = wb.active
                    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
                        
                        if row[1].value in ids_error_muestras:
                            for cell in row:
                                cell.fill = openpyxl.styles.PatternFill(start_color="FF0000", end_color="FF0000", fill_type = "solid")
                        elif row[1].value in ids_formato_incorrecto:
                            for cell in row:
                                if cell.col_idx - 1 in columna_errores_formato:
                                    cell.fill = openpyxl.styles.PatternFill(start_color="FF8000", end_color="FF8000", fill_type = "solid")
                        elif row[1].value in ids_campos_vacios:
                            for cell in row:
                                if cell.value == None:
                                    cell.fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type = "solid")
                        elif row[1].value in ids_localizaciones_ocupadas:
                            for cell in row:
                                cell.fill = openpyxl.styles.PatternFill(start_color="51D1F6", end_color="51D1F6", fill_type = "solid")
                       
                    output = io.BytesIO()    
                    wb.save(output)
                    wb.close()
                    response = HttpResponse(output.getvalue(),content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="listado_errores.xlsx"'
                    return response        
 
    else:
        form = UploadExcel(request)     
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

def descargar_plantilla(request,macro:int):
    # Vista para descargar la plantilla de Excel para subir localizaciones o muestras
    if macro == 0:
        plantilla_path = os.path.join(settings.BASE_DIR, 'datos_prueba', 'globalstaticfiles', 'plantilla_localizaciones.xlsx')
        if os.path.exists(plantilla_path):
            return FileResponse(open(plantilla_path, 'rb'), as_attachment=True, filename='plantilla_localizaciones.xlsx')
    elif macro == 1:
        plantilla_path = os.path.join(settings.BASE_DIR, 'datos_prueba', 'globalstaticfiles', 'plantilla_localizaciones_macros.xlsm')
        if os.path.exists(plantilla_path):
            return FileResponse(open(plantilla_path, 'rb'), as_attachment=True, filename='plantilla_localizaciones_macros.xlsm')
    elif macro == 2:
        plantilla_path = os.path.join(settings.BASE_DIR, 'datos_prueba', 'globalstaticfiles', 'plantilla_muestras.xlsx')
        if os.path.exists(plantilla_path):
            return FileResponse(open(plantilla_path, 'rb'), as_attachment=True, filename='plantilla_muestras.xlsx')
    else:
        return HttpResponse("La plantilla no se encuentra disponible.", status=404)
    
# Vistas para Localizacion

def localizaciones(request):
    # Vista que muestra todas las localizaciones, tengan o no muestra
    localizaciones = Localizacion.objects.all().values().distinct()
    congeladores = Localizacion.objects.exclude(congelador=None).values_list('congelador', flat=True).distinct()
    
    estantes = (Localizacion.objects.exclude(estante='')
                .values_list('congelador','estante')
                .distinct())
    
    posicion_estante = (Localizacion.objects.exclude(posicion_rack_estante='')
                       .values_list('congelador','estante','posicion_rack_estante')
                       .distinct())
    
    racks = (Localizacion.objects.exclude(rack='')
             .values_list('congelador','estante','posicion_rack_estante','rack')
             .distinct())
    
    posiciones_caja_rack = (Localizacion.objects.exclude(posicion_caja_rack='')
                           .values_list('congelador','estante','posicion_rack_estante','rack','posicion_caja_rack')
                           .distinct())
    
    cajas = (Localizacion.objects.exclude(caja='')
             .values_list('congelador','estante','posicion_rack_estante','rack','posicion_caja_rack','caja')
             .distinct())
    
    subposiciones = (Localizacion.objects
                    .values_list('congelador','estante','posicion_rack_estante','rack','posicion_caja_rack','caja','subposicion')
                    .distinct())
    
    muestras = (Localizacion.objects
                .values_list('congelador','estante','posicion_rack_estante','rack','posicion_caja_rack','caja','subposicion','muestra')
                .distinct().order_by('subposicion'))
    template = loader.get_template('localizaciones_todas.html')
    
    param = ['congelador', 'estante', 'posicion_rack_estante', 'rack', 'posicion_caja_rack', 'caja', 'subposicion']
    # Convertimos las claves de request.GET a un set para búsquedas rápidas
    keys = set(request.GET.keys())

    # Lista de niveles y sus nombres en orden jerárquico
    niveles = [
        (congeladores, "congelador"),
        (estantes, "estante"),
        (posicion_estante, "posicion_rack_estante"),
        (racks, "rack"),
        (posiciones_caja_rack, "posicion_caja_rack"),
        (cajas, "caja"),
        (subposiciones, "subposicion"),
    ]

    # Inicializamos flag para saber si se ejecutó alguna combinación completa
    combinacion_ejecutada = False

    # Procesamos primero combinaciones completas (subposiciones)
    for subpos in subposiciones:
        claves_combinacion = [f'{nombre}{subpos[i]}' for i, (nivel, nombre) in enumerate(niveles)]  # excluimos id/subposicion final
        if all(clave in keys for clave in claves_combinacion):
            eliminar_localizacion(request, "|".join([str(s) for s in subpos]), "subposicion")
            combinacion_ejecutada = True

    # Si no se ejecutó ninguna combinación completa, procesamos niveles parciales de arriba hacia abajo
    
    if not combinacion_ejecutada:
        for nivel, nombre in reversed(niveles[:-1]):  # excluimos subposiciones para procesarlas solo en combinaciones completas
            for elemento in nivel:
                key= []
                # Construimos la clave según la estructura de cada nivel
                if isinstance(elemento, tuple):
                    key_values = [str(e) for e in elemento]
                    for i, (niv, nom) in enumerate(niveles):
                        if i < len(elemento):
                            key.append(f'{nom}{elemento[i]}')
                else:
                    key = [f'{nombre}{elemento}']
                    key_values = [str(elemento)]

                if all(clave in keys for clave in key):
                    eliminar_localizacion(request, "|".join(key_values), nombre)
                    combinacion_ejecutada = True
                    break
            if combinacion_ejecutada:
                break

    context = {
        'localizaciones': localizaciones,
        'congeladores': congeladores,
        'estantes': estantes,
        'posicion_estante': posicion_estante,
        'racks': racks,
        'posiciones_caja_rack': posiciones_caja_rack,   
        'cajas': cajas,
        'muestras': muestras  
    }
    return HttpResponse(template.render(context, request))

def upload_excel_localizaciones(request):
    if request.method=="POST":
        form = UploadExcel(request.POST, request.FILES)
        if 'confirmar' in request.POST:
            messages.success(request, 'Las localizaciones se han añadido correctamente.')
            
        elif 'cancelar' in request.POST:
            # Eliminación de las muestras añadidas del excel
            ids_to_delete = request.session.pop('nuevos_ids', [])
            Localizacion.objects.filter(id__in=ids_to_delete).delete()
        elif 'excel_file' in request.FILES:
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file)
                rename_columns = {
                    'Congelador': 'congelador', 
                    'Estante': 'estante',
                    'Posición del rack en el estante': 'posicion_rack_estante',
                    'Rack': 'rack',
                    'Posición de la caja en el rack': 'posicion_caja_rack',
                    'Caja': 'caja',
                    'Subposición': 'subposicion'
                }
                df.rename(columns=rename_columns, inplace=True)
                errors = 0
                nuevos_ids = []
                for _, row in df.iterrows():
                    try:
                        localizacion, created = Localizacion.objects.update_or_create(
                            congelador=row['congelador'],
                            estante=row['estante'], 
                            posicion_rack_estante=row['posicion_rack_estante'],
                            rack=row['rack'],
                            posicion_caja_rack=row['posicion_caja_rack'],
                            caja=row['caja'],
                            subposicion=row['subposicion']    
                        )
                        if created:
                            nuevos_ids.append(localizacion.id)
                        else:
                            messages.info(request, f'Localizacion {localizacion} ya existe, el excel no se ha procesado correctamente')
                            errors+=1
                    except ValueError:
                        messages.error(request, f'El formato de alguno de los campos de la localizacion {localizacion} no es el correcto. Revisa el formato de los datos.')
                        errors+=1
                        redirect('localizacion_nueva')
                request.session['nuevos_ids'] = nuevos_ids
                nuevos_ids = []
                if errors==0:
                    messages.success(request, 'El archivo excel es correcto.')
                else:
                    messages.warning(request, f'El archivo excel contiene {errors} errores.') 
                return redirect('localizaciones_todas') 
    else:
        form = UploadExcel(request)     
    return render(request, 'localizacion_nueva.html', {'form': form}) 

def eliminar_localizacion(request, loc, param):
    # Vista para eliminar una localización específica
    if param == 'congelador':
        localizaciones = Localizacion.objects.filter(congelador=loc)
        localizaciones.delete()

    elif param == 'estante':
        congelador,estante = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante)
        field_names = [f.name for f in Localizacion._meta.local_fields if f.name not in ('congelador','muestra','id')]
        for unit in localizaciones:
            for field in field_names:    
                setattr(unit, field, '')
            Localizacion.objects.filter(estante='').delete()
            unit.save()

    elif param == 'posicion_rack_estante':
        congelador, estante, posicion_rack_estante = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante, posicion_rack_estante=posicion_rack_estante)
        field_names = [f.name for f in Localizacion._meta.local_fields if f.name not in ('congelador','muestra','id','estante')]
        for unit in localizaciones:
            for field in field_names:    
                setattr(unit, field, '')
            Localizacion.objects.filter(posicion_rack_estante='').delete()
            unit.save() 

    elif param == 'rack':
        congelador, estante, posicion_rack_estante, rack = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante, posicion_rack_estante=posicion_rack_estante, rack=rack)
        field_names = [f.name for f in Localizacion._meta.local_fields if f.name not in ('congelador','muestra','id','estante','posicion_rack_estante')]
        for unit in localizaciones:
            for field in field_names:    
                setattr(unit, field, '')
            Localizacion.objects.filter(rack='').delete()
            unit.save()

    elif param == 'posicion_caja_rack':
        congelador, estante, posicion_rack_estante, rack, posicion_caja_rack = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante, posicion_rack_estante=posicion_rack_estante, rack=rack, posicion_caja_rack=posicion_caja_rack)
        field_names = [f.name for f in Localizacion._meta.local_fields if f.name not in ('congelador','muestra','id','estante','posicion_rack_estante','rack')]
        for unit in localizaciones:
            for field in field_names:    
                setattr(unit, field, '')
            Localizacion.objects.filter(posicion_caja_rack='').delete()
            unit.save()

    elif param == 'caja':
        congelador, estante, posicion_rack_estante, rack, posicion_caja_rack, caja = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante, posicion_rack_estante=posicion_rack_estante, rack=rack, posicion_caja_rack=posicion_caja_rack, caja=caja)
        field_names = [f.name for f in Localizacion._meta.local_fields if f.name not in ('congelador','muestra','id','estante','posicion_rack_estante','rack','posicion_caja_rack')]
        for unit in localizaciones:
            for field in field_names:    
                setattr(unit, field, '')
            Localizacion.objects.filter(caja='').delete()
            unit.save()

    elif param == 'subposicion':
        congelador, estante, posicion_rack_estante, rack, posicion_caja_rack, caja, subposicion = loc.split('|')
        localizaciones = Localizacion.objects.filter(congelador=congelador, estante=estante, posicion_rack_estante=posicion_rack_estante, rack=rack, posicion_caja_rack=posicion_caja_rack, caja=caja, subposicion=subposicion)
        for unit in localizaciones:
            unit.muestra = None
            unit.save()
    
    else:
        return redirect('archivo/')
    
    return redirect('archivo/')

@transaction.atomic
def archivar_muestra(request):
    # Vista para archivar una muestra en una localización específica que esté vacía 
    if request.method == 'POST':
        form = archivar_muestra_form(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            try:
                muestra_obj = data['muestra']
                if Localizacion.objects.filter(muestra=muestra_obj):
                    new = Localizacion.objects.select_for_update().get(muestra=muestra_obj)
                    new.muestra = None
                    new.save()
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

                historial = historial_localizaciones.objects.create(muestra=muestra_obj, localizacion=slot,
                                                                    fecha_asignacion=timezone.now(), usuario_asignacion=request.user)
                
                historial.save()
                return redirect('localizaciones_todas') 
                
            except Muestra.DoesNotExist:
                
                messages.error(request, "Error interno: La muestra no fue encontrada.")
            
            except Localizacion.DoesNotExist:
                 
                messages.error(request, "Error interno: La ubicación ya no está disponible o no existe.")
                
    else:
        form =  archivar_muestra_form()
        
    context = {'form': form}
    return render(request, 'archivar_muestra.html', context)
def historial_localizaciones_muestra(request,muestra_id):
    muestra = Muestra.objects.get(id=muestra_id)
    historiales = historial_localizaciones.objects.filter(muestra=muestra).order_by('-fecha_asignacion')
    if muestra.estado_actual=='Destruida':
        estado_destruccion = registro_destruido.objects.get(muestra=muestra)
    template = loader.get_template('historial_localizaciones.html')
    return HttpResponse(template.render({'historiales':historiales, 'muestra':muestra, 'estado_destruccion':estado_destruccion},request))

# Vistas relacionadas con el modelo estudio
def estudios_todos(request):
    if request.user.groups.filter(name='Investigadores'):
        estudios = Estudio.objects.filter(investigador_principal__username=request.user.username)
    else:
        estudios = Estudio.objects.all()
    template = loader.get_template('estudios_todos.html')
    context = {
        'estudios':estudios
    }
    return HttpResponse(template.render(context,request))

def nuevo_estudio(request):
    if request.method == 'POST':
        form = EstudioForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('estudios_todos')
        else:
            messages.error(request, 'Hubo un error al subir el documento.')
    else:
        form = EstudioForm()
    template = loader.get_template('nuevo_estudio.html')
    return HttpResponse(template.render({'form':form},request))

def seleccionar_estudio(request):
    if request.user.groups.filter(name='Investigadores'):
        estudios = Estudio.objects.filter(investigador_principal__username=request.user.username)
    else:
        estudios = Estudio.objects.all()
    template = loader.get_template('seleccionar_estudio.html')
    return HttpResponse(template.render({'estudios':estudios},request))

def añadir_muestras_estudio(request):
    if request.method == 'POST':
        muestras = request.session.get('muestras_estudio', [])
        ids_estudios = request.POST.getlist('estudio_id')
        for study in ids_estudios:
            studio = Estudio.objects.get(nombre_estudio=study)
            muestras=Muestra.objects.filter(id__in=muestras)
            for muestra in muestras:
                if muestra.estado_actual != 'Destruida':
                    muestra.estudio = studio
                    muestra.save()
                    if historial_estudios.objects.filter(muestra=muestra,estudio=studio).exists():
                        pass
                    else:   
                        historial = historial_estudios.objects.create(
                            muestra = muestra,
                            estudio = studio,
                            fecha_asignacion = timezone.now(),
                            usuario_asignacion = request.user
                        )
                        historial.save()
        if 'muestras_estudio' in request.session:
            del request.session['muestras_estudio']
        return redirect('muestras_todas')
    return redirect('muestras_todas')

def historial_estudios_muestra(request,muestra_id):
    muestra = Muestra.objects.get(id=muestra_id)
    historiales = historial_estudios.objects.filter(muestra=muestra).order_by('-fecha_asignacion')
    template = loader.get_template('historial_estudios.html')
    return HttpResponse(template.render({'historiales':historiales, 'muestra':muestra},request))

def repositorio_estudio(request, id_estudio):
    estudio = Estudio.objects.get(id_estudio=id_estudio)
    documentos = Documento.objects.filter(estudio = estudio, eliminado= False)
    request.session['id_estudio'] = id_estudio
    # Filtrado opcional por usuario
    usuario = request.GET.get('usuario')
    if usuario:
        documentos = documentos.filter(usuario_subida__username=usuario)
    # Filtrado opcional por categoría
    categoria = request.GET.get('categoria')
    if categoria:
        documentos = documentos.filter(categoria__icontains=categoria)
    for doc in documentos:    
        if request.GET.get(f'{doc.id}'):
            eliminar_documento(request, doc.id)
    template = loader.get_template('repositorio_estudio.html')
    return HttpResponse(template.render({'documentos':documentos, 'id_estudio':estudio.id_estudio},request))

def subir_documento(request, id_estudio):
    estudio = Estudio.objects.get(id_estudio = id_estudio)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.usuario_subida = request.user
            doc.save()
            messages.success(request, f'Documento "{doc.archivo.name}" subido correctamente.')
        else:
            messages.error(request, 'Hubo un error al subir el documento.')
    else:
        form = DocumentoForm()
    template = loader.get_template('subir_documento.html')
    return HttpResponse(template.render({'form':form, 'estudio':estudio},request))

def descargar_documento(request, documento_id,id_estudio):
    doc = Documento.objects.get(pk=documento_id, eliminado=False)      
    return FileResponse(open(doc.archivo.path, 'rb'), as_attachment=True, filename=os.path.basename(doc.archivo.name))

def eliminar_documento(request):
    ids_documento = request.POST.getlist('doc_id')
    for element in ids_documento:
        try:
            doc = Documento.objects.get(pk=element, eliminado=False)
            doc.eliminado = True
            doc.fecha_eliminacion = timezone.now()
            doc.save()
            return redirect('repositorio_estudio', id_estudio=doc.estudio)
        except:
            return redirect('repositorio_estudio', id_estudio=doc.estudio.id_estudio)
    return redirect('repositorio_estudio', id_estudio=request.session.get('id_estudio'))

# Vistas relacionadas con el envio de muestras

def formulario_envios(request,centro):
    muestras_envio = request.session.get('muestras_envio', [])
    centro_envio = agenda_envio.objects.get(id=centro)
    muestras = Muestra.objects.filter(id__in=muestras_envio, volumen_actual__gt=0)
    template = loader.get_template('formulario_envios.html')
    return HttpResponse(template.render({'muestras':muestras,'centro':centro_envio},request))

def upload_excel_envios(request,centro):
    if request.method=='POST':
        form = UploadExcel(request.POST, request.FILES)
        if 'descargar_excel_envio' in request.POST:
            centro_envio = agenda_envio.objects.get(id=centro)
            muestras = request.session.get('muestras_envio',[])
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="listado_envio.xlsx"'
            wb = openpyxl.load_workbook(os.path.join(settings.BASE_DIR, 'datos_prueba', 'globalstaticfiles', 'plantilla_envios.xlsx'))
            ws = wb.active
            row_num = 2
            for muestra in muestras:
                sample = Muestra.objects.get(id=muestra)
                if sample.estado_actual != 'Destruida':
                    ws.cell(row_num,1).value=str(sample.nom_lab)
                    ws.cell(row_num,2).value=str(sample.volumen_actual) + ' ' + str(sample.unidad_volumen)
                    ws.cell(row_num,3).value=str(sample.concentracion_actual) + ' ' + str(sample.unidad_concentracion)
                    ws.cell(row_num,5).value=str(sample.unidad_volumen)
                    ws.cell(row_num,7).value=str(sample.unidad_concentracion)
                    ws.cell(row_num,8).value=str(centro_envio.centro)
                    ws.cell(row_num,9).value=str(centro_envio.lugar)
                    row_num +=1 
            wb.save(response)
            return response
        elif 'excel_file' in request.FILES:
            if form.is_valid():
                ids_errores_envio = []
                errores_envio= 0
                errores_campos_vacios=0
                errores_formato = 0
                ids_errores_formato = []
                ids_errores_campos_vacios = []
                numero_registros = 0
                excel_file = request.FILES['excel_file']
                excel_bytes = excel_file.read()
                request.session['excel_file_name'] = excel_file.name
                request.session['excel_file_base64']= base64.b64encode(excel_bytes).decode()
                excel_stream = io.BytesIO(excel_bytes)
                df = pd.read_excel(excel_stream)
                rename_columns = {
                    'Muestra':'muestra',
                    'Volumen enviado':'volumen_enviado', 
                    'Concentración enviada':'concentracion_enviada',
                    'Centro de destino':'centro_destino',
                    'Lugar de destino':'lugar_destino'
                }
                df.rename(columns=rename_columns, inplace=True)
                for _, row in df.iterrows():
                    try:
                        instancia_muestra = Muestra.objects.get(nom_lab=row['muestra'])
                        envio = Envio.objects.create(muestra=instancia_muestra,
                                                    volumen_enviado=row['volumen_enviado'],
                                                    unidad_volumen_enviado=instancia_muestra.unidad_volumen,
                                                    concentracion_enviada=row['concentracion_enviada'],
                                                    centro_destino=row['centro_destino'],
                                                    unidad_concentracion_enviada=instancia_muestra.unidad_concentracion,
                                                    lugar_destino=row['lugar_destino'],
                                                    fecha_envio=timezone.now(),
                                                    usuario_envio=request.user
                                                    )
                        envio.save()
                        numero_registros += 1
                        if float(row['volumen_enviado']) == instancia_muestra.volumen_actual:
                            instancia_muestra.volumen_actual = 0
                            instancia_muestra.concentracion_actual = 0
                            instancia_muestra.estado_actual = 'Enviada'
                            instancia_muestra.save()
                            if Localizacion.objects.filter(muestra=instancia_muestra).exists():
                                loc = Localizacion.objects.get(muestra=instancia_muestra)
                                loc.muestra = None
                                loc.save()
                        elif float(row['volumen_enviado']) > instancia_muestra.volumen_actual:
                            ids_errores_envio.append(instancia_muestra.nom_lab)
                            errores_envio += 1
                            envio.delete()
                        else:
                            instancia_muestra.volumen_actual -= float(row['volumen_enviado'])
                            instancia_muestra.estado_actual = 'Parcialmente enviada'
                            instancia_muestra.save()
                    except ValueError:
                        errores_formato += 1
                        ids_errores_formato.append(instancia_muestra.nom_lab)
                        numero_registros+=1
                    except ProgrammingError:
                        errores_campos_vacios += 1
                        ids_errores_campos_vacios.append(instancia_muestra.nom_lab)
                        numero_registros+=1
                if 'muestras_envio' in request.session:
                    del request.session['muestras_envio']
                request.session['ids_errores_formato'] = ids_errores_formato
                request.session['ids_errores_envio'] = ids_errores_envio
                request.session['ids_errores_campos_vacios']= ids_errores_campos_vacios
                messages.info(request, f'El excel subido tiene {numero_registros} registros.')
                if errores_envio==0 and errores_campos_vacios==0 and errores_formato==0:
                    messages.success(request, 'Y no tiene errores en ningún campo.')
                else:
                    messages.warning(request, f'Y contiene {errores_envio} errores en el volumen de envio de algunas muestras, {errores_formato} errores de formato y {errores_campos_vacios} campos vacios.')
                return render(request,'confirmacion_upload_envio.html') 
        elif 'excel_errores' in request.POST:
                ids_errores_envio = request.session.get('ids_errores_envio', [])
                ids_errores_campos_vacios= request.session.get('ids_errores_campos_vacios',[])
                ids_errores_formato=request.session.get('ids_errores_formato',[])
                excel_bytes = base64.b64decode(request.session.get('excel_file_base64'))
                excel_file = io.BytesIO(excel_bytes)
                wb = openpyxl.load_workbook(excel_file)
                ws = wb.active
                for row in ws.iter_rows(min_row=2, max_row=ws.max_row):

                    if row[0].value in ids_errores_campos_vacios:
                        for cell in row:
                            cell.fill = openpyxl.styles.PatternFill(start_color="FF8000", end_color="FF8000", fill_type = "solid")
                    elif row[0].value in ids_errores_formato:
                        for cell in row:
                            cell.fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type = "solid")
                    elif row[0].value in ids_errores_envio:
                        for cell in row:
                            cell.fill = openpyxl.styles.PatternFill(start_color="FF0000", end_color="FF0000", fill_type = "solid")
                    
                output = io.BytesIO()    
                wb.save(output)
                wb.close()
                response = HttpResponse(output.getvalue(),content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="listado_errores_envio.xlsx"'
                return response         
    else:
        form = UploadExcel(request)
    template = loader.get_template('upload_excel_envios.html')     
    return HttpResponse(template.render({'form': form},request))

def registrar_envio(request,centro):
    if request.method=='POST':
        centro_envio = agenda_envio.objects.get(id=centro)
        muestras = request.session.get('muestras_envio', [])
        volumen_enviado_form = request.POST.getlist('volumen_enviado')
        concentracion_enviada_form = request.POST.getlist('concentracion_enviada')
        centro_destino_form = centro_envio.centro
        lugar_destino_form = centro_envio.lugar
        iterar = 0
        for muestra in muestras:
            instancia_muestra = Muestra.objects.get(id=muestra)
            envio = Envio.objects.create(
                muestra=instancia_muestra,
                fecha_envio=timezone.now(),
                volumen_enviado = volumen_enviado_form[iterar],
                unidad_volumen_enviado = instancia_muestra.unidad_volumen,
                concentracion_enviada = concentracion_enviada_form[iterar],
                unidad_concentracion_enviada = instancia_muestra.unidad_concentracion,
                centro_destino = centro_destino_form,
                lugar_destino=lugar_destino_form,
                usuario_envio = request.user
            )
            envio.save()
            if float(volumen_enviado_form[iterar]) >= instancia_muestra.volumen_actual:
                instancia_muestra.volumen_actual = 0
                instancia_muestra.concentracion_actual = 0
                instancia_muestra.estado_actual = 'Enviada'
                instancia_muestra.save()
                if Localizacion.objects.filter(muestra=instancia_muestra).exists():
                    loc = Localizacion.objects.get(muestra=instancia_muestra)
                    loc.muestra = None
                    loc.save()
            else:
                instancia_muestra.volumen_actual -= float(volumen_enviado_form[iterar])
                instancia_muestra.estado_actual = 'Parcialmente enviada'
                instancia_muestra.save()
            iterar += 1
        if 'muestras_envio' in request.session:
            del request.session['muestras_envio']
        return redirect('muestras_todas')
    return redirect('formulario_envios')

def historial_envios(request,muestra_id):
    sample = Muestra.objects.get(id=muestra_id)
    envios = Envio.objects.filter(muestra=sample).order_by('-fecha_envio')
    volumen_original = sample.volumen_actual + sum(envio.volumen_enviado for envio in envios)
    volumen_restante = sample.volumen_actual
    template = loader.get_template('historial_envios.html')
    context = {
        'muestra':sample,
        'envios':envios,
        'volumen_original':volumen_original,
        'volumen_restante':volumen_restante
    }
    return HttpResponse(template.render(context,request))

def agenda(request):
    agenda_envios = agenda_envio.objects.all()
    template = loader.get_template('agenda.html')
    return HttpResponse(template.render({'agenda':agenda_envios},request))

def nuevo_centro(request):
    if request.method == 'POST':
        form = Centroform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agenda')
        else:
            messages.error(request, 'Hubo un error al añadir el centro.')
    else:
        form = Centroform()
    template = loader.get_template('nuevo_centro.html')
    return HttpResponse(template.render({'form':form},request))

def editar_centro(request, id_centro):
    centro = agenda_envio.objects.get(id=id_centro)
    if request.method == 'POST':
        form = Centroform(request.POST, instance=centro)
        if form.is_valid():
            form.save()
            return redirect('agenda')
    else:
        form = Centroform(instance=centro)
    return render(request, 'editar_centro.html', {'form': form, 'centro': centro})

def eliminar_centro(request):
    if request.method=="POST":
        ids = request.POST.getlist('ids_centro')
        for centro_id in ids:
            centro = agenda_envio.objects.get(id=centro_id)
            centro.delete()
    return redirect('agenda')