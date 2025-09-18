from django.contrib import admin
from .models import Usuario
# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email')
    search_fields = ('nombre', 'email')
    list_filter = ('nombre',)
admin.site.register(Usuario, UsuarioAdmin)