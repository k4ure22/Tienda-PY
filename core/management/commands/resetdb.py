from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Producto, SolicitudRegistro, SolicitudCompra

class Command(BaseCommand):
    help = "Limpia la base de datos y deja solo el admin por defecto"

    def handle(self, *args, **kwargs):
        Usuario = get_user_model()

        # Eliminar todas las tablas relacionadas con tu sistema
        Producto.objects.all().delete()
        SolicitudRegistro.objects.all().delete()
        SolicitudCompra.objects.all().delete()
        Usuario.objects.exclude(email="admin@correo.com").delete()

        # Verificar que el admin siga existiendo
        if not Usuario.objects.filter(email="admin@correo.com").exists():
            admin = Usuario.objects.create_superuser(
                nombre="Administrador",
                email="admin@correo.com",
                password="admin123"
            )
            admin.cargo = "Administrador"
            admin.save()

        self.stdout.write(self.style.SUCCESS("✅ Base de datos reseteada. Admin por defecto listo."))
