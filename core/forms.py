from django import forms
from .models import Producto, Usuario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'marca',
            'modelo',
            'almacenamiento',
            'ram',
            'procesador',
            'serial',
            'precio',
            'color',
            'detalles',
            'imagen'
        ]

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre", "edad", "cargo", "email", "foto_perfil"]
