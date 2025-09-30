from django import forms
from .models import Peticion, Tema, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ["titulo", "mensaje"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe el asunto"}),
            "mensaje": forms.Textarea(attrs={"class": "form-control", "placeholder": "Describe tu petición..."}),
        }



class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["titulo", "contenido"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título del nuevo tema"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe el contenido de tu tema..."}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe tu comentario...", "rows": 3}),
        }
        labels = {
            "contenido": "Comentario",
        }

class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya está en uso.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
