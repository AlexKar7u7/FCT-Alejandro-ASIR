"""
URL configuration for mi_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("articulos/", views.lista_articulos, name="lista_articulos"),
    path("articulos/<int:articulo_id>/me_interesa/", views.me_interesa, name="me_interesa"),
    path("peticion/", views.nueva_peticion, name="nueva_peticion"),
    path("contacto/", views.contacto, name="contacto"),
    path("aviso_legal/", views.aviso_legal, name="aviso_legal"),

    # login / logout
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="inicio"), name="logout"),

    # register
    path("register/", views.register, name="register"),

    # propuestas y votos
    path("propuestas/", views.lista_propuestas, name="lista_propuestas"),
    path("votar/<int:propuesta_id>/<int:valor>/", views.votar, name="votar"),


    path("temas/", views.lista_temas, name="lista_temas"),
    path("temas/nuevo/", views.nuevo_tema, name="nuevo_tema"),
    path("temas/<int:tema_id>/", views.detalle_tema, name="detalle_tema"),
    path("temas/<int:tema_id>/comentar/", views.nuevo_comentario, name="nuevo_comentario"),
    path("comentarios/<int:comentario_id>/borrar/", views.borrar_comentario, name="borrar_comentario"),


    path("guias/", views.lista_guias, name="lista_guias"),
    path("guias/nueva/", views.nueva_guia, name="nueva_guia"),
    path("guias/<int:guia_id>/", views.detalle_guia, name="detalle_guia"),
    path("guias/oficiales/", views.lista_guias_oficiales, name="lista_guias_oficiales"),
    path("guias/<int:guia_id>/editar/", views.editar_guia, name="editar_guia"),
    path("guias/<int:guia_id>/borrar/", views.borrar_guia, name="borrar_guia"),
]
