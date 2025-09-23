from django.shortcuts import render
from django.http import HttpResponse
from .models import Muestra
from django.template import loader
# Create your views here.
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def muestras_todas(request):
    muestras = Muestra.objects.all().values()
    template = loader.get_template('muestras_todas.html')
    context = {
        'muestras': muestras,
    }
    return HttpResponse(template.render(context, request))