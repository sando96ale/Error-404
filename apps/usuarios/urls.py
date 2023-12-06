from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    
    path('registro/', views.Registro.as_view(), name = 'registro'),

    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),

    path('cambio-contrasena/', views.cambio_contrasena, name='cambio_contrasena'),
]