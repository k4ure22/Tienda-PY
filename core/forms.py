from django import forms
from .models import Producto, Usuario, SolicitudRegistro, SolicitudCompra

base_input = "w-full px-4 py-2 mt-1 rounded-xl border border-gray-300 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"

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
        widgets = {
            "marca": forms.TextInput(attrs={"class": base_input}),
            "modelo": forms.TextInput(attrs={"class": base_input}),
            "almacenamiento": forms.NumberInput(attrs={"class": base_input}),
            "ram": forms.NumberInput(attrs={"class": base_input}),
            "procesador": forms.TextInput(attrs={"class": base_input}),
            "serial": forms.TextInput(attrs={"class": base_input}),
            "precio": forms.NumberInput(attrs={"class": base_input}),
            "color": forms.TextInput(attrs={"class": base_input}),
            "detalles": forms.Textarea(attrs={"class": base_input + " h-24 resize-none"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-gray-700 mt-2"}),
        }


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": base_input,
            "placeholder": "Ingrese una nueva contraseña (opcional)"
        })
    )

    class Meta:
        model = Usuario
        fields = ["nombre", "edad", "email", "foto_perfil", "password"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": base_input}),
            "edad": forms.NumberInput(attrs={"class": base_input}),
            "email": forms.EmailInput(attrs={"class": base_input}),
            "foto_perfil": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-gray-700 mt-2"}),
        }


class SolicitudRegistroForm(forms.ModelForm):
    class Meta:
        model = SolicitudRegistro
        fields = [
            "nombres", "tipo_identificacion", "numero_identificacion",
            "edad", "direccion", "correo", "telefono", "cargo"
        ]
        widgets = {
            "nombres": forms.TextInput(attrs={"class": base_input}),
            "tipo_identificacion": forms.Select(attrs={"class": base_input}),  
            "numero_identificacion": forms.TextInput(attrs={"class": base_input}),
            "edad": forms.NumberInput(attrs={"class": base_input}),
            "direccion": forms.TextInput(attrs={"class": base_input}),
            "correo": forms.EmailInput(attrs={"class": base_input}),
            "telefono": forms.TextInput(attrs={"class": base_input}),
        }



class SolicitudCompraForm(forms.ModelForm):
    class Meta:
        model = SolicitudCompra
        fields = [
            'cliente_nombre',
            'cliente_cedula',
            'cliente_telefono',
            'cliente_direccion',
            'cliente_correo',
            'metodo_pago',
        ]
        widgets = {
            "cliente_nombre": forms.TextInput(attrs={"class": base_input}),
            "cliente_cedula": forms.TextInput(attrs={"class": base_input}),
            "cliente_telefono": forms.TextInput(attrs={"class": base_input}),
            "cliente_direccion": forms.TextInput(attrs={"class": base_input}),
            "cliente_correo": forms.EmailInput(attrs={"class": base_input}),
            "metodo_pago": forms.Select(attrs={"class": base_input}),
        }
