from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.titulo} (x{self.cantidad})"
    
class Peticion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # quién hizo la petición
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)  # para marcar si ya se revisó

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"