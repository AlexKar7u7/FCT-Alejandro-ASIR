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
from .models import Propuesta, Voto, Tema, Comentario
from .forms import TemaForm, ComentarioForm


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

def lista_temas(request):
    """Muestra la lista de todos los temas creados."""
    temas = Tema.objects.all().order_by('-fecha_creacion')
    return render(request, 'blog/lista_temas.html', {'temas': temas})

@login_required
def nuevo_tema(request):
    """Permite a los usuarios crear un nuevo tema."""
    if request.method == "POST":
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.autor = request.user
            tema.save()
            messages.success(request, "El tema ha sido creado con éxito.")
            return redirect("detalle_tema", tema_id=tema.id) 
    else:
        form = TemaForm()
    return render(request, "blog/nuevo_tema.html", {"form": form})

def detalle_tema(request, tema_id):
    """Muestra un tema, sus comentarios de nivel superior, y el formulario para un nuevo comentario."""
    tema = get_object_or_404(Tema, id=tema_id)
    
    # Filtramos solo los comentarios de nivel superior (aquellos sin padre)
    comentarios_principales = tema.comentarios.filter(parent__isnull=True)
    
    form = ComentarioForm()
    
    return render(request, 'blog/detalle_tema.html', {
        'tema': tema,
        'comentarios': comentarios_principales, # Enviamos solo los comentarios principales
        'form': form, # El formulario de comentario principal
    })

@login_required
def nuevo_comentario(request, tema_id):
    """Procesa el formulario para añadir un nuevo comentario o una respuesta."""
    tema = get_object_or_404(Tema, id=tema_id)
    
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tema = tema
            comentario.autor = request.user
            
            # Lógica para manejar la respuesta a otro comentario (anidamiento)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comentario.parent = Comentario.objects.get(id=parent_id)
                except Comentario.DoesNotExist:
                    messages.error(request, "El comentario al que intentas responder no existe.")
                    return redirect('detalle_tema', tema_id=tema_id)
            
            comentario.save()
            messages.success(request, "Comentario publicado con éxito.")
            return redirect('detalle_tema', tema_id=tema_id)
    
    messages.error(request, "No se pudo publicar el comentario.")
    return redirect('detalle_tema', tema_id=tema_id)

@login_required
def borrar_comentario(request, comentario_id):
    """Permite al usuario borrar un comentario si es el autor."""
    comentario = get_object_or_404(Comentario, id=comentario_id)
    tema_id = comentario.tema.id  # Guardar el ID del tema para redirigir
    
    # 1. Verificar que el usuario es el autor del comentario
    if comentario.autor == request.user:
        comentario.delete()
        messages.success(request, "El comentario ha sido borrado con éxito.")
    else:
        # 2. Si no es el autor, se prohíbe la acción
        messages.error(request, "No tienes permiso para borrar este comentario.")
        
    return redirect('detalle_tema', tema_id=tema_id)