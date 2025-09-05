from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate

def crear_admin_defecto(sender, **kwargs):
    Usuario = get_user_model()

    # Verificar si ya existe
    if not Usuario.objects.filter(email="admin@correo.com").exists():
        # Crear superuser
        admin = Usuario.objects.create_superuser(
            nombre="Administrador",
            username="admin",
            email="martinmh0722@gmail.com",
            password="admin123"
        )
        admin.cargo = "admin" 
        admin.save()

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(crear_admin_defecto, sender=self)
