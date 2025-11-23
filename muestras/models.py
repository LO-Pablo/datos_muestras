from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
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
    estado_inicial = models.CharField(max_length=50, 
                                      choices=[('CONG','Congelado'), ('REF','Refrigerado'), ('AMB','Ambiente')],blank=True, null=True)
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
    congelador = models.CharField(max_length=50)
    estante = models.CharField(max_length=50,blank=True)
    posicion_rack_estante = models.CharField(max_length=50,blank=True)
    rack = models.CharField(max_length=50,blank=True)
    posicion_caja_rack = models.CharField(max_length=50,blank=True)
    caja = models.CharField(max_length=50,blank=True)
    subposicion = models.IntegerField(blank=True)

    class Meta:
        # Campos unicos de localización en conjunción
        unique_together = ('muestra','congelador', 'estante', 'posicion_rack_estante', 'rack', 'posicion_caja_rack', 'caja', 'subposicion')

    def __str__(self):
        return f"{self.congelador} - {self.estante} - {self.posicion_rack_estante} - {self.rack} - {self.posicion_caja_rack} - {self.caja} - {self.subposicion}"
    
class Estudio(models.Model):
    # Campos del modelo Estudio
    id_estudio = models.CharField(max_length=20, unique=True)
    referencia_estudio = models.CharField(max_length=100, blank=True, null=True)
    nombre_estudio = models.CharField(max_length=100,unique=True)
    descripcion_estudio = models.TextField(blank=True, null=True)
    fecha_inicio_estudio = models.DateField(blank=True, null=True)
    fecha_fin_estudio = models.DateField(blank=True, null=True)
    investigador_principal = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return f"Estudio {self.nombre_estudio}"
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

    def __str__(self):
        return f"Envio de Muestra {self.id_individuo} - {self.nom_lab} el {self.fecha_envio}"