from django.shortcuts import render
from .models import Articulo

# Create your views here.
def lista_articulos(request):
    articulos = Articulo.objects.all()  # SELECT * FROM blog_articulo
    return render(request, 'blog/lista.html', {'articulos': articulos})

def inicio(request):
    return render(request, 'blog/inicio.html')