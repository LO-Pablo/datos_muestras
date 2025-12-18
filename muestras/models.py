from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
class Muestra(models.Model):
    # Campos del modelo Muestra
    id_individuo = models.CharField(max_length=20)
    nom_lab = models.CharField(max_length=100, unique=True)
    id_material = models.CharField(max_length=20,blank=True, null=True)
    volumen_actual = models.FloatField(blank=True, null=True)
    unidad_volumen = models.CharField(max_length=15,blank=True, null=True)
    concentracion_actual = models.FloatField(blank=True, null=True)
    unidad_concentracion = models.CharField(max_length=15,blank=True, null=True)
    masa_actual = models.FloatField(blank=True, null=True)
    unidad_masa = models.CharField(max_length=15,blank=True, null=True)
    fecha_extraccion = models.DateField(blank=True, null=True)
    fecha_llegada = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado_inicial = models.CharField(max_length=50,blank=True, null=True)
    centro_procedencia = models.CharField(max_length=100,blank=True, null=True)
    lugar_procedencia = models.CharField(max_length=100,blank=True, null=True)
    estado_actual = models.CharField(max_length=50, default='Disponible',
                                        choices=[('DISP','Disponible'), ('ENV','Enviada'), ('ENVP','Parcialmente enviada'), ('DEST','Destruida')],blank=True, null=True)
    estudio = models.ForeignKey('Estudio', blank=True, to_field='nombre_estudio', on_delete=models.SET_NULL, null=True)
    class Meta:
        # Definición de permisos personalizados para el modelo Muestra
        permissions = [
            ("can_view_muestras_web", "Puede ver muestras en la web"),
            ("can_add_muestras_web", "Puede añadir muestras en la web"),
            ("can_change_muestras_web", "Puede cambiar muestras en la web"),
            ("can_delete_muestras_web", "Puede eliminar muestras en la web"),
        ]
        
    def __str__(self):
        return f"{self.id_individuo} - {self.nom_lab}"

class Localizacion(models.Model):
    # Campos del modelo Localizacion, que referencia a una muestra
    muestra = models.ForeignKey('Muestra',to_field = "nom_lab",related_name="localizacion", blank=True, null=True, on_delete=models.SET_NULL)
    congelador = models.CharField(max_length=50, blank=True, null=True)
    estante = models.CharField(max_length=50,blank=True, null=True)
    posicion_rack_estante = models.CharField(max_length=50,blank=True, null=True)
    rack = models.CharField(max_length=50,blank=True, null=True)
    posicion_caja_rack = models.CharField(max_length=50,blank=True, null=True)
    caja = models.CharField(max_length=50,blank=True, null=True)
    subposicion = models.IntegerField(blank=True, null=True)

    class Meta:
        # Campos unicos de localización en conjunción
        unique_together = ('muestra','congelador', 'estante', 'posicion_rack_estante', 'rack', 'posicion_caja_rack', 'caja', 'subposicion')
        permissions = [
            ("can_view_localizaciones_web", "Puede ver localizaciones en la web"),
            ("can_add_localizaciones_web", "Puede añadir localizaciones en la web"),
            ("can_change_localizaciones_web", "Puede cambiar localizaciones en la web"),
            ("can_delete_localizaciones_web", "Puede eliminar localizaciones en la web"),
        ]
    def __str__(self):
        return f"{self.congelador} - {self.estante} - {self.posicion_rack_estante} - {self.rack} - {self.posicion_caja_rack} - {self.caja} - {self.subposicion}"


class Congelador(models.Model):
    congelador = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50,blank=True, null=True)
    temperatura_minima = models.CharField(max_length=50,blank=True, null=True)
    temperatura_maxima = models.CharField(max_length=50,blank=True, null=True)
    localizacion_edificio = models.CharField(max_length=50,blank=True, null=True)
    fotografia = models.ImageField(upload_to='congeladores/', blank=True, null=True)
class historial_localizaciones(models.Model):
    muestra = models.ForeignKey('Muestra',related_name="historial_localizaciones",on_delete=models.CASCADE)
    localizacion = models.ForeignKey('Localizacion',related_name="historial_localizaciones",on_delete=models.SET_NULL, null=True, blank=True)
    fecha_asignacion = models.DateField(default=timezone.now) 
    usuario_asignacion = models.ForeignKey(User,on_delete=models.PROTECT, blank=True, null=True)   

class registro_destruido(models.Model):
    muestra = models.ForeignKey('Muestra',related_name="estado_destruido",on_delete=models.CASCADE)
    fecha = models.DateField(default = timezone.now)
    usuario = models.ForeignKey(User,on_delete=models.PROTECT, blank=True, null=True)
class Estudio(models.Model):
    # Campos del modelo Estudio
    referencia_estudio = models.CharField(max_length=100, blank=True, null=True)
    nombre_estudio = models.CharField(max_length=100,unique=True)
    descripcion_estudio = models.TextField(blank=True, null=True)
    fecha_inicio_estudio = models.DateField(blank=True, null=True)
    fecha_fin_estudio = models.DateField(blank=True, null=True)
    investigador_principal = models.CharField(max_length=100, blank=True, null=True)
    investigadores_asociados = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'groups__name': 'Investigadores'},related_name="estudios_asignados",blank = True)
    class Meta:
        permissions = [
            ("can_view_estudios_web", "Puede ver estudios en la web"),
            ("can_add_estudios_web", "Puede añadir estudios en la web"),
            ("can_change_estudios_web", "Puede cambiar estudios en la web"),
            ("can_delete_estudios_web", "Puede eliminar estudios en la web"),
        ]
    def __str__(self):
        return f"Estudio {self.nombre_estudio}"
class historial_estudios(models.Model):
    muestra = models.ForeignKey('Muestra',related_name="historial_estudios",on_delete=models.CASCADE)
    estudio = models.ForeignKey('Estudio',related_name="historial_estudios",on_delete=models.CASCADE, blank=True, null=True)
    fecha_asignacion = models.DateField(default=timezone.now)
    usuario_asignacion = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True) 

def ruta_documentos(instance,filename):
    return f"estudios/{instance.estudio.id_estudio}/{filename}"
class Documento(models.Model):
    estudio = models.ForeignKey('Estudio',related_name = "estudio", on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=ruta_documentos)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(blank=True, null=True, max_length=50)
    usuario_subida = models.ForeignKey(User,on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default = False)
    fecha_eliminacion = models.DateField(blank = True, null=True)
class Envio(models.Model):
    # Campos del modelo Envio, que referencia a una muestra
    muestra = models.ForeignKey('Muestra',related_name="envio",on_delete=models.CASCADE)
    volumen_enviado = models.FloatField()
    unidad_volumen_enviado = models.CharField(max_length=15)
    concentracion_enviada = models.FloatField()
    unidad_concentracion_enviada = models.CharField(max_length=15)
    centro_destino = models.CharField(max_length=100)
    lugar_destino = models.CharField(max_length=100)
    fecha_envio = models.DateField(default=timezone.now)
    usuario_envio = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"Envio de Muestra {self.id_individuo} - {self.nom_lab} el {self.fecha_envio}"
    
class agenda_envio(models.Model):
    centro = models.CharField(max_length=200,unique=True,default=None)
    lugar=models.CharField(max_length=200)
    direccion=models.TextField()
    persona_contacto = models.CharField(max_length=200,blank=True, null=True)
    telefono_contacto=models.IntegerField(blank=True, null=True)