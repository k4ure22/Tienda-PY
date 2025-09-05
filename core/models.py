from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(null=True, blank=True)
    CARGO_CHOICES = [
        ("cliente", "Cliente"),
        ("admin", "Administrador"),
    ]
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default="cliente")    
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(
        upload_to="fotos_perfil/",
        blank=True,
        null=True,
        default="usuarios/perfil.png"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']   # 👈 Django te pedirá username igual

    def __str__(self):
        return self.email



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

class Venta(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=100)
    cliente_cedula = models.CharField(max_length=20)
    cliente_telefono = models.CharField(max_length=20)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos/")

    def __str__(self):
        return f"Imagen de {self.marca} {self.modelo}"
    

class SolicitudRegistro(models.Model):
    nombres = models.CharField(max_length=150)
    tipo_identificacion = models.CharField(max_length=20)
    numero_identificacion = models.CharField(max_length=50)
    edad = models.IntegerField()
    direccion = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.nombres} ({self.cargo})"
    
class SolicitudCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=150)
    cliente_cedula = models.CharField(max_length=50)
    cliente_telefono = models.CharField(max_length=20)
    cliente_direccion = models.CharField(max_length=255)
    cliente_correo = models.EmailField()
    metodo_pago = models.CharField(
        max_length=50,
        choices=[
            ("tarjeta_credito", "Tarjeta de Crédito"),
            ("tarjeta_debito", "Tarjeta de Débito"),
            ("transferencia", "Transferencia Bancaria"),
            ("efectivo", "Efectivo"),
        ],
        default="tarjeta_credito"
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.producto.marca} {self.producto.modelo} por {self.cliente_nombre}"
