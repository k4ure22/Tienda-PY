from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']


    def __str__(self):
        return self.nombre
    



class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    Categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    especificaciones = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.nombre
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos/")

    def __str__(self):
        return f"Imagende {self.producto.nombre}"