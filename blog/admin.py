from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Articulo
from .models import Peticion

admin.site.register(Articulo)

@admin.register(Peticion)
class PeticionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "fecha", "atendida")
    list_filter = ("atendida", "fecha")
    search_fields = ("titulo", "usuario__username")