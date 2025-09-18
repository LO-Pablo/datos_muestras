from django.db import models
from django.conf import settings
from django.utils import timezone

class Muestra(models.Model):
    id_individuo = models.CharField(max_length=20)
    nom_lab = models.CharField(max_length=100)
    id_material = models.CharField(max_length=20)
    volumen_actual = models.FloatField()
    unidad_volumen = models.CharField(max_length=10)
    concentracion_actual = models.FloatField()
    unidad_concentracion = models.CharField(max_length=10)
    masa_actual = models.FloatField()
    unidad_masa = models.CharField(max_length=10)
    fecha_extraccion = models.DateField()
    fecha_llegada = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    estado_inicial = models.CharField(max_length=50, 
                                      choices=[('CONG','Congelado'), ('REF','Refrigerado'), ('AMB','Ambiente')])
    centro_procedencia = models.CharField(max_length=100)
    lugar_procedencia = models.CharField(max_length=100)

    def __str__(self):
        return f"Muestra {self.id_individuo} - {self.nom_lab}"