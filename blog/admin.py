from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Articulo
from .models import Peticion
from .models import Propuesta, Voto
from .models import Tema, Comentario

admin.site.register(Articulo)
admin.site.register(Propuesta)
admin.site.register(Voto)
admin.site.register(Tema)
admin.site.register(Comentario)

@admin.register(Peticion)
class PeticionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "fecha", "atendida")
    list_filter = ("atendida", "fecha")
    search_fields = ("titulo", "usuario__username")