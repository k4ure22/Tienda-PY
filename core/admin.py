from django.contrib import admin
from .models import SolicitudRegistro

# Register your models here.

@admin.register(SolicitudRegistro)
class SolicitudRegistroAdmin(admin.ModelAdmin):
    list_display = ("nombres", "numero_identificacion", "correo", "cargo", "fecha_solicitud")
