from django.http import HttpResponse
from .models import Muestra, Localizacion, Estudio, Envio
from django.template import loader
from .forms import MuestraForm, LocalizacionForm
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required


def principal(request):
    # Vista principal de la aplicación, muestra una página de bienvenida
    template = loader.get_template('principal.html')
    return HttpResponse(template.render(request=request))
@login_required
def muestras_todas(request):
    # Vista que muestra todas las muestras, requiere que el usuario esté autenticado
    muestras = Muestra.objects.prefetch_related('localizacion')
    template = loader.get_template('muestras_todas.html')
    localizacion = Localizacion.objects.all().values()
    context = {    
        'muestras': muestras,
        'localizacion': localizacion,
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
    