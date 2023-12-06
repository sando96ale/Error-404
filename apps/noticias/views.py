from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria, Comentario
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from .forms import CrearNoticiaForm

def es_personal(user):
    return user.is_staff

def Listar_Noticias(request):
    contexto = {}

    id_categoria = request.GET.get('id', None)
    orden = request.GET.get('orden', None)

    noticias = Noticia.objects.all()

    if id_categoria:
        noticias = noticias.filter(categoria_noticia=id_categoria)

    if orden == 'asc':
        noticias = noticias.order_by('fecha')
    elif orden == 'desc':
        noticias = noticias.order_by('-fecha')
    elif orden == 'alpha_asc':
        noticias = noticias.order_by('titulo')
    elif orden == 'alpha_desc':
        noticias = noticias.order_by('-titulo')

    contexto['noticias'] = noticias

    cat = Categoria.objects.all().order_by('nombre')
    contexto['categorias'] = cat

    return render(request, 'noticias/listar.html', contexto)



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

    
    if not comentario.puede_modificar(request.user):
        return HttpResponseBadRequest("No tienes permisos para modificar este comentario.")

    if request.method == 'POST':
        nuevo_texto = request.POST.get('nuevo_texto', None)

        
        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()

            
            return redirect('noticias:detalle', pk=comentario.noticia.pk)

    
    return render(request, 'noticias/modificar_comentario.html', {'comentario': comentario})


def crear_noticia(request):
    if request.method == 'POST':
        formulario = CrearNoticiaForm(request.POST, request.FILES)
        if formulario.is_valid():
            nueva_noticia = formulario.save()
            return redirect('noticias:detalle', pk=nueva_noticia.pk) 
    else:
        formulario = CrearNoticiaForm()

    return render(request, 'noticias/crear_noticia.html', {'formulario': formulario})

@user_passes_test(es_personal)
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    noticia.delete()
    return redirect('noticias:listar')

@user_passes_test(es_personal)
def eliminar_comentario2(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    comentario.delete()
    return redirect('noticias:detalle', pk=comentario.noticia.pk)

@user_passes_test(es_personal)
def Modificar_Comentario2(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    # Verificar si el usuario es staff o el autor del comentario
    if request.user.is_staff or request.user == comentario.usuario:
        if request.method == 'POST':
            nuevo_texto = request.POST.get('nuevo_texto', None)

            if nuevo_texto:
                comentario.texto = nuevo_texto
                comentario.save()

                return redirect('noticias:detalle', pk=comentario.noticia.pk)

        return render(request, 'noticias/modificar_comentario.html', {'comentario': comentario})
    else:
        # Si no es staff ni el autor del comentario, redirige a alguna página de error o muestra un mensaje
        return HttpResponseBadRequest("No tienes permisos para modificar este comentario.")

@user_passes_test(es_personal)
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    if request.method == 'POST':
        formulario = CrearNoticiaForm(request.POST, request.FILES, instance=noticia)
        if formulario.is_valid():
            formulario.save()
            return redirect('noticias:detalle', pk=noticia.pk)
    else:
        formulario = CrearNoticiaForm(instance=noticia)

    return render(request, 'noticias/editar_noticia.html', {'formulario': formulario, 'noticia': noticia})

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