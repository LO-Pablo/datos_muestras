from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.principal, name='principal'),
    path('muestras/', views.muestras_todas, name='muestras_todas'),
]