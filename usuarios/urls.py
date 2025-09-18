from django.urls import path
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/detalles_usuario/<int:id>', views.detalles_usuario, name='detalles_usuario'),
    path('testing/', views.testing, name='testing'),
]