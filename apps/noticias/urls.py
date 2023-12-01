
from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
	
	path('', views.Listar_Noticias, name = 'listar'),
    
	path('', views.Inicio, name='inicio'),

	path('Detalle/<int:pk>', views.Detalle_Noticias, name = 'detalle'),
	
	path('Comentario/', views.Comentar_Noticia, name = 'comentar'),
	
	path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    
	path('modificar_comentario/<int:comentario_id>/', views.Modificar_Comentario, name='modificar_comentario'),
]