from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria, Comentario
from django.urls import reverse_lazy
import random
from django.http import HttpResponseBadRequest

@login_required
def Listar_Noticias(request):
	contexto = {}

	id_categoria = request.GET.get('id',None)

	if id_categoria:
		n = Noticia.objects.filter(categoria_noticia = id_categoria)
	else:
		n = Noticia.objects.all() #RETORNA UNA LISTA DE OBJETOS

	contexto['noticias'] = n

	cat = Categoria.objects.all().order_by('nombre')
	contexto['categorias'] = cat

	return render(request, 'noticias/listar.html', contexto)

@login_required
def Detalle_Noticias(request, pk):
	contexto = {}

	n = Noticia.objects.get(pk = pk) #RETORNA SOLO UN OBEJTO
	contexto['noticia'] = n

	c = Comentario.objects.filter(noticia = n)
	contexto['comentarios'] = c

	return render(request, 'noticias/detalle.html',contexto)



@login_required
def Comentar_Noticia(request):

	com = request.POST.get('comentario',None)
	usu = request.user
	noti = request.POST.get('id_noticia', None)# OBTENGO LA PK
	noticia = Noticia.objects.get(pk = noti) #BUSCO LA NOTICIA CON ESA PK
	coment = Comentario.objects.create(usuario = usu, noticia = noticia, texto = com)

	return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))


@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if request.user == comentario.usuario:
        comentario.delete()
    return redirect('noticias:detalle', pk=comentario.noticia.pk)


@login_required
def Modificar_Comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    # Verificar si el usuario es el propietario del comentario
    if not comentario.puede_modificar(request.user):
        return HttpResponseBadRequest("No tienes permisos para modificar este comentario.")

    if request.method == 'POST':
        nuevo_texto = request.POST.get('nuevo_texto', None)

        # Modificar el comentario si el nuevo texto es válido
        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()

            # Redirigir a la página de detalle después de la modificación
            return redirect('noticias:detalle', pk=comentario.noticia.pk)

    # Renderizar el formulario de modificación si no se ha enviado el formulario
    return render(request, 'noticias/modificar_comentario.html', {'comentario': comentario})


@login_required
def Inicio(request):
    contexto = {}

    # Obtener las 5 noticias más recientes ordenadas por fecha descendente
    noticias_recientes = Noticia.objects.all().order_by('-fecha')[:5]
    contexto['noticias'] = noticias_recientes

    # Obtener todas las categorías
    cat = Categoria.objects.all().order_by('nombre')
    contexto['categorias'] = cat

    return render(request, 't_home.html', contexto)


#{'nombre':'name', 'apellido':'last name', 'edad':23}
#EN EL TEMPLATE SE RECIBE UNA VARIABLE SEPARADA POR CADA CLAVE VALOR
# nombre
# apellido
# edad

'''
ORM

CLASE.objects.get(pk = ____)
CLASE.objects.filter(campos = ____)
CLASE.objects.all() ---> SELECT * FROM CLASE

'''