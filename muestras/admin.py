from django.contrib import admin
from .models import Muestra, Localizacion, Estudio, Envio, Documento,historial_estudios,historial_localizaciones,registro_destruido

admin.site.register(Muestra)
admin.site.register(Localizacion)
admin.site.register(Estudio)
admin.site.register(Envio)
admin.site.register(Documento)
admin.site.register(historial_estudios)
admin.site.register(historial_localizaciones)
admin.site.register(registro_destruido)