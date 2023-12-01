from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

