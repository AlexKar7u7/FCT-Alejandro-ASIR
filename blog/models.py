from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField(default=0)

    interesados = models.ManyToManyField(User, related_name='articulos_interesados', blank=True)

    def __str__(self):
        return f"{self.titulo} (x{self.cantidad})"
    
class Peticion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    atendida = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    

class Propuesta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def votos_positivos(self):
        return self.votos.filter(valor=True).count()

    def votos_negativos(self):
        return self.votos.filter(valor=False).count()

class Voto(models.Model):
    propuesta = models.ForeignKey(Propuesta, related_name="votos", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.BooleanField()  

    class Meta:
        unique_together = ("propuesta", "usuario")  

class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model):
    tema = models.ForeignKey(Tema, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='respuestas', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.tema.titulo}"
    
    class Meta:
        ordering = ['fecha_creacion'] 