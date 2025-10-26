from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.principal, name='principal'),
    path('muestras/', views.muestras_todas, name='muestras_todas'),
    path('muestras/nueva', views.añadir_muestras, name='añadir_muestras'),
    path('muestras/upload_excel', views.upload_excel, name='upload_excel'),
    path('muestras/upload_excel/descargar', views.descargar_plantilla, name='descargar_plantilla'),
    path('archivo/detalles_muestra/<str:nom_lab>', views.detalles_muestra, name='detalles_muestra'),
    path('muestras/detalles_muestra/<str:id_individuo>/<str:nom_lab>/editar', views.editar_muestra, name='editar_muestra'),
    path('muestras/detalles_muestra/<str:id_individuo>/<str:nom_lab>/eliminar', views.eliminar_muestra, name='eliminar_muestra'),
    path('archivo/', views.localizaciones, name='localizaciones_todas'),
    path('archivo/nuevo', views.nueva_localizacion, name='localizaciones_nueva'),
    path('archivo/archivar_muestra', views.archivar_muestra, name='archivar_muestra'),
]