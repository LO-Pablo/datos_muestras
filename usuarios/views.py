from django.http import HttpResponse
from django.template import loader
from .models import Usuario
def usuarios(request):
    myusuarios = Usuario.objects.all().values()
    template = loader.get_template('usuarios_all.html')
    context = {
        'myusuarios': myusuarios,
    }
    return HttpResponse(template.render(context, request))
def detalles_usuario(request, id):
    myusuario = Usuario.objects.get(id=id)
    template = loader.get_template('detalles_usuario.html')
    context = {
        'myusuario': myusuario,
    }
    return HttpResponse(template.render(context, request))
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['apple', 'banana', 'cherry'],
    }
    return HttpResponse(template.render(context, request))