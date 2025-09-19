from django import forms
from .models import Peticion

class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ["titulo", "mensaje"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe el asunto"}),
            "mensaje": forms.Textarea(attrs={"class": "form-control", "placeholder": "Describe tu petición..."}),
        }
