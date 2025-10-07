from django.http import HttpResponse
from .models import Muestra
from django.template import loader
from .forms import MuestraForm
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

def principal(request):
    template = loader.get_template('principal.html')
    return HttpResponse(template.render(request=request))
@login_required
def muestras_todas(request):
    muestras = Muestra.objects.all().values()
    template = loader.get_template('muestras_todas.html')
    context = {
        'muestras': muestras,
    }
    return HttpResponse(template.render(context, request))
@login_required
@permission_required('muestras.can_view_muestras')
def detalles_muestra(request, id_individuo, nom_lab):
    muestra = Muestra.objects.get(id_individuo=id_individuo, nom_lab=nom_lab)
    template = loader.get_template('detalles_muestra.html')
    context = {
        'muestra': muestra,
    }
    return HttpResponse(template.render(context, request))
@permission_required('muestras.can_add_muestras')
def nueva_muestra(request):
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_muestra', id_individuo=form.instance.id_individuo, nom_lab=form.instance.nom_lab)
    else:
        form = MuestraForm()
    return render(request, 'nueva_muestra.html', {'form': form})
@permission_required('muestras.can_change_muestras')
def editar_muestra(request, id_individuo, nom_lab):
    muestra = Muestra.objects.get(id_individuo=id_individuo, nom_lab=nom_lab)
    if request.method == 'POST':
        form = MuestraForm(request.POST, instance=muestra)
        if form.is_valid():
            form.save()
            return redirect('detalles_muestra', id_individuo=form.instance.id_individuo, nom_lab=form.instance.nom_lab)
    else:
        form = MuestraForm(instance=muestra)
    return render(request, 'editar_muestra.html', {'form': form, 'muestra': muestra})
@permission_required('muestras.can_delete_muestras')
def eliminar_muestra(request, id_individuo, nom_lab):
    muestra = get_object_or_404(Muestra,id_individuo=id_individuo, nom_lab=nom_lab)
    muestra.delete()
    return redirect('muestras_todas')
    