from django.shortcuts import render, redirect
from .models import Articulo
from django.contrib.auth.decorators import login_required
from .forms import PeticionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def lista_articulos(request):
    articulos = Articulo.objects.all()  # SELECT * FROM blog_articulo
    return render(request, 'blog/lista.html', {'articulos': articulos})

def inicio(request):
    return render(request, 'blog/inicio.html')


def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'blog/lista.html', {'articulos': articulos})

@login_required
def nueva_peticion(request):
    if request.method == "POST":
        form = PeticionForm(request.POST)
        if form.is_valid():
            peticion = form.save(commit=False)
            peticion.usuario = request.user
            peticion.save()
            return redirect("inicio")  # redirige a donde quieras
    else:
        form = PeticionForm()
    return render(request, "blog/nueva_peticion.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu cuenta ha sido creada con éxito. Ahora puedes iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "blog/register.html", {"form": form})
