from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    cargo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to="usuarios/", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']

    def __str__(self):
        return self.email


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    almacenamiento = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    procesador = models.CharField(max_length=100)
    serial = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True, null=True)
    detalles = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"



class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos/")

    def __str__(self):
        return f"Imagen de {self.marca} {self.modelo}"