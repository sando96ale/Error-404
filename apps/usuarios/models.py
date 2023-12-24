from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class PerfilUsuario(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfilusuario')
