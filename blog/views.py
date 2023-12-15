from django.shortcuts import render
from apps.noticias.models import Noticia

#request 'es un diccionario que continuamente se va pasando entre el navegador y el servidor'

def Home(request):
	ultimas_noticias = Noticia.objects.order_by('-fecha')[:4]

	return render(request, 't_home.html', {'ultimas_noticias': ultimas_noticias})


def Nosotros(request):

	return render(request, 't_nosotros.html')

def Contacto(request):
	
	return render(request, 't_contacto.html')


