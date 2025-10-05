from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.principal, name='principal'),
    path('muestras/', views.muestras_todas, name='muestras_todas'),
    path('muestras/nueva', views.nueva_muestra, name='nueva_muestra'),
    path('muestras/detalles_muestra/<str:id_individuo>/<str:nom_lab>', views.detalles_muestra, name='detalles_muestra'),
    path('muestras/detalles_muestra/<str:id_individuo>/<str:nom_lab>/editar', views.editar_muestra, name='editar_muestra'),
    path('muestras/detalles_muestra/<str:id_individuo>/<str:nom_lab>/eliminar', views.eliminar_muestra, name='eliminar_muestra'),
]