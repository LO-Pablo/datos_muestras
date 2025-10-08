from django.db import models
from django.conf import settings
from django.utils import timezone

class Muestra(models.Model):
    # Campos del modelo Muestra
    id_individuo = models.CharField(max_length=20, unique=True)
    nom_lab = models.CharField(max_length=100, unique=True)
    id_material = models.CharField(max_length=20)
    volumen_actual = models.FloatField()
    unidad_volumen = models.CharField(max_length=15)
    concentracion_actual = models.FloatField()
    unidad_concentracion = models.CharField(max_length=15)
    masa_actual = models.FloatField()
    unidad_masa = models.CharField(max_length=15)
    fecha_extraccion = models.DateField()
    fecha_llegada = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    estado_inicial = models.CharField(max_length=50, 
                                      choices=[('CONG','Congelado'), ('REF','Refrigerado'), ('AMB','Ambiente')])
    centro_procedencia = models.CharField(max_length=100)
    lugar_procedencia = models.CharField(max_length=100)
    estado_actual = models.CharField(max_length=50, default='Disponible',
                                        choices=[('DISP','Disponible'), ('ENV','Enviada'), ('ENVP','Parcialmente enviada'), ('DEST','Destruida')])

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
    muestra = models.ForeignKey('Muestra', 
                                     related_name="localizacion",
                                     on_delete=models.CASCADE)
    congelador = models.CharField(max_length=50)
    estante = models.CharField(max_length=50)
    posicion_rack_estante = models.CharField(max_length=50)
    rack = models.CharField(max_length=50)
    posicion_caja_rack = models.CharField(max_length=50)
    caja = models.CharField(max_length=50)
    subposicion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.congelador} - {self.estante} - {self.posicion_rack_estante} - {self.rack} - {self.posicion_caja_rack} - {self.caja} - {self.subposicion}"
    
class Estudio(models.Model):
    # Campos del modelo Estudio, que referencia a una muestra
    id_individuo = models.ForeignKey(Muestra, to_field= "id_individuo", 
                                     related_name="id_inidividuo_estudio",
                                     on_delete=models.CASCADE)
    nom_lab = models.ForeignKey(Muestra,to_field="nom_lab", 
                                related_name="nom_lab_estudio",
                                on_delete=models.CASCADE)
    id_estudio = models.CharField(max_length=20)
    referencia_estudio = models.CharField(max_length=100)
    nombre_estudio = models.CharField(max_length=100)
    descripcion_estudio = models.TextField(blank=True, null=True)
    fecha_inicio_estudio = models.DateField()
    fecha_fin_estudio = models.DateField(blank=True, null=True)
    investigador_principal = models.CharField(max_length=100)

    def __str__(self):
        return f"Estudio {self.nombre_estudio} para Muestra {self.id_individuo} - {self.nom_lab}"

class Envio(models.Model):
    # Campos del modelo Envio, que referencia a una muestra
    id_individuo = models.ForeignKey(Muestra, to_field= "id_individuo",
                                     related_name="id_inidividuo_envio",
                                     on_delete=models.CASCADE)
    nom_lab = models.ForeignKey(Muestra, to_field="nom_lab",
                                related_name="nom_lab_envio",
                                on_delete=models.CASCADE)
    volumen_enviado = models.FloatField()
    unidad_volumen_enviado = models.CharField(max_length=15)
    concentracion_enviada = models.FloatField()
    unidad_concentracion_enviada = models.CharField(max_length=15)
    centro_destino = models.CharField(max_length=100)
    lugar_destino = models.CharField(max_length=100)

    def __str__(self):
        return f"Envio de Muestra {self.id_individuo} - {self.nom_lab} el {self.fecha_envio}"