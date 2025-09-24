from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo
from django.contrib.auth.decorators import login_required
from .forms import PeticionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import redirect
from .models import Propuesta, Voto


# Create your views here.
def lista_articulos(request):
    articulos = Articulo.objects.all()  # SELECT * FROM blog_articulo
    return render(request, 'blog/lista.html', {'articulos': articulos})

def inicio(request):
    return render(request, 'blog/inicio.html')


def lista_articulos(request):
    articulos = Articulo.objects.all()
    # Verificar si el usuario está autenticado antes de intentar filtrar
    if request.user.is_authenticated:
        for articulo in articulos:
            # Añade una propiedad booleana a cada artículo
            articulo.is_interesado = articulo.interesados.filter(id=request.user.id).exists()
    else:
        # Si no está autenticado, todos los artículos no están "interesados"
        for articulo in articulos:
            articulo.is_interesado = False
            
    return render(request, 'blog/lista.html', {'articulos': articulos})

@login_required
def me_interesa(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if articulo.interesados.filter(id=request.user.id).exists():
        articulo.interesados.remove(request.user)  # Si ya está interesado, lo elimina
    else:
        articulo.interesados.add(request.user)     # Si no está interesado, lo añade
    
    return redirect('lista_articulos')

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



def lista_propuestas(request):
    propuestas = Propuesta.objects.all()
    return render(request, "blog/propuestas.html", {"propuestas": propuestas})

@login_required
def votar(request, propuesta_id, valor):
    propuesta = get_object_or_404(Propuesta, id=propuesta_id)
    voto, created = Voto.objects.update_or_create(
        propuesta=propuesta, usuario=request.user,
        defaults={"valor": valor}
    )
    return redirect("lista_propuestas")