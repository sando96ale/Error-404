
from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
	
	path('', views.Listar_Noticias, name = 'listar'),

	path('Detalle/<int:pk>', views.Detalle_Noticias, name = 'detalle'),
	
	path('Comentario/', views.Comentar_Noticia, name = 'comentar'),
	
	path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    
	path('modificar_comentario/<int:comentario_id>/', views.Modificar_Comentario, name='modificar_comentario'),
    
	path('crear_noticia/', views.crear_noticia, name='crear_noticia'),
    
	path('eliminar_noticia/<int:pk>/', views.eliminar_noticia, name='eliminar_noticia'),
    
	path('editar_noticia/<int:pk>/', views.editar_noticia, name='editar_noticia'),
    
	path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario2, name='eliminar_comentario'),
    
	path('modificar_comentario/<int:comentario_id>/', views.Modificar_Comentario2, name='modificar_comentario'),
    
]