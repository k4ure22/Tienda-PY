from django import forms
from .models import Producto, Usuario, SolicitudRegistro, SolicitudCompra

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
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["nombre", "edad", "cargo", "email", "foto_perfil", "password"]

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data["email"]  # ← aquí rellenamos username
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario


class SolicitudRegistroForm(forms.ModelForm):
    class Meta:
        model = SolicitudRegistro
        fields = [
            "nombres", "tipo_identificacion", "numero_identificacion",
            "edad", "direccion", "correo", "telefono", "cargo"
        ]
        widgets = {
            "tipo_identificacion": forms.Select(choices=[
                ("CC", "Cédula de Ciudadanía"),
                ("TI", "Tarjeta de Identidad"),
                ("CE", "Cédula de Extranjería"),
            ])
        }

class SolicitudCompraForm(forms.ModelForm):
    class Meta:
        model = SolicitudCompra
        fields = ['nombre', 'cedula', 'telefono', 'direccion']