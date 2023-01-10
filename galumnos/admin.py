from django.contrib import admin

from galumnos.models import *

class ClienteAlumno(admin.ModelAdmin):
    list_display = ("rut","nombre","apellidop","apellidom","telefono","email")
    search_fields = ("nombre",)
    list_filter = ("apellidop",)

class ClienteModulos(admin.ModelAdmin):
    list_display = ("nombremodulo","carrera","docente","nhoras")


admin.site.register(Alumnos, ClienteAlumno)
admin.site.register(Modulos, ClienteModulos)



