# En el archivo noticias/forms.py
from django import forms
from .models import Noticia

class CrearNoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'cuerpo', 'imagen', 'categoria_noticia']
