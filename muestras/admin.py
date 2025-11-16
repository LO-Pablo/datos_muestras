from django.contrib import admin
from .models import Muestra, Localizacion, Estudio, Envio

admin.site.register(Muestra)
admin.site.register(Localizacion)
admin.site.register(Estudio)
admin.site.register(Envio)
