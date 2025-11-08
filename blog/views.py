from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo
from django.contrib.auth.decorators import login_required
from .forms import PeticionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import RegistroForm, UserUpdateForm
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import redirect
from .models import Propuesta, Voto, Tema, Comentario, Guia
from .forms import TemaForm, ComentarioForm, GuiaForm


def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'blog/lista.html', {'articulos': articulos})

def inicio(request):
    return render(request, 'blog/inicio.html')

def contacto(request):
    return render(request, 'blog/contacto.html')

def aviso_legal(request):
    return render(request, 'blog/aviso_legal.html')


def lista_articulos(request):
    articulos = Articulo.objects.all()
    if request.user.is_authenticated:
        for articulo in articulos:
            articulo.is_interesado = articulo.interesados.filter(id=request.user.id).exists()
    else:
        for articulo in articulos:
            articulo.is_interesado = False
            
    return render(request, 'blog/lista.html', {'articulos': articulos})

@login_required
def me_interesa(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if articulo.interesados.filter(id=request.user.id).exists():
        articulo.interesados.remove(request.user)  
    else:
        articulo.interesados.add(request.user)     
    
    return redirect('lista_articulos')

@login_required
def nueva_peticion(request):
    if request.method == "POST":
        form = PeticionForm(request.POST)
        if form.is_valid():
            peticion = form.save(commit=False)
            peticion.usuario = request.user
            peticion.save()
            return redirect("inicio")  
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
    return render(request, "auth/register.html", {"form": form})

@login_required
def perfil_usuario(request):
    """Mostrar y permitir la edición del perfil del usuario autenticado.

    GET: mostrar el formulario con los datos actuales.
    POST: validar y guardar cambios, luego redirigir al mismo perfil con un mensaje.
    """
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado con éxito.")
            return redirect('perfil_usuario')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "auth/user.html", {"usuario": request.user, "form": form})



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
    
    comentarios_principales = tema.comentarios.filter(parent__isnull=True)
    
    form = ComentarioForm()
    
    return render(request, 'blog/detalle_tema.html', {
        'tema': tema,
        'comentarios': comentarios_principales, 
        'form': form, 
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
    tema_id = comentario.tema.id  
    
    if comentario.autor == request.user:
        comentario.delete()
        messages.success(request, "El comentario ha sido borrado con éxito.")
    else:
        messages.error(request, "No tienes permiso para borrar este comentario.")
        
    return redirect('detalle_tema', tema_id=tema_id)


def lista_guias(request):
    """Muestra la lista de todas las guías creadas."""
    guias = Guia.objects.all().order_by('-fecha_creacion')
    return render(request, 'blog/lista_guias.html', {'guias': guias})

@login_required
def nueva_guia(request):
    """Permite a los usuarios crear una nueva guía."""
    if request.method == "POST":
        form = GuiaForm(request.POST)
        if form.is_valid():
            guia = form.save(commit=False)
            guia.autor = request.user
            guia.save()
            messages.success(request, "La guía ha sido creada con éxito.")
            return redirect("detalle_guia", guia_id=guia.id)
    else:
        form = GuiaForm()
    return render(request, "blog/nueva_guia.html", {"form": form})

def detalle_guia(request, guia_id):
    """Muestra el contenido de una guía."""
    guia = get_object_or_404(Guia, id=guia_id)
    return render(request, 'blog/detalle_guia.html', {'guia': guia})

def lista_guias_oficiales(request):
    """Muestra solo las guías creadas por administradores (is_staff)."""
    guias_oficiales = Guia.objects.filter(autor__is_staff=True).order_by('-fecha_creacion')
    return render(request, 'blog/lista_guias_oficiales.html', {'guias': guias_oficiales})


@login_required
def editar_guia(request, guia_id):
    """Permite al autor de la guía editar su contenido."""
    guia = get_object_or_404(Guia, id=guia_id)
    
    # 1. Restricción de Autoría
    if guia.autor != request.user:
        messages.error(request, "No tienes permiso para editar esta guía.")
        return redirect('detalle_guia', guia_id=guia.id)

    if request.method == "POST":
        # Al editar, pasamos la instancia para que el formulario se pre-cargue y actualice
        form = GuiaForm(request.POST, instance=guia)
        if form.is_valid():
            form.save()
            # El campo ultima_modificacion se actualiza automáticamente (auto_now=True)
            messages.success(request, "La guía ha sido actualizada con éxito.")
            return redirect('detalle_guia', guia_id=guia.id)
    else:
        form = GuiaForm(instance=guia)
    
    return render(request, "blog/editar_guia.html", {"form": form, "guia": guia})

@login_required
def borrar_guia(request, guia_id):
    """Permite al autor de la guía borrarla."""
    guia = get_object_or_404(Guia, id=guia_id)
    
    # 1. Restricción de Autoría
    if guia.autor != request.user:
        messages.error(request, "No tienes permiso para borrar esta guía.")
        return redirect('detalle_guia', guia_id=guia.id)

    # 2. El borrado se procesa solo con una solicitud POST para seguridad
    if request.method == "POST":
        guia.delete()
        messages.success(request, f"La guía '{guia.titulo}' ha sido eliminada.")
        return redirect('lista_guias')
        
    # Si alguien intenta acceder por GET, lo redirigimos a la página de detalle
    return redirect('detalle_guia', guia_id=guia.id)