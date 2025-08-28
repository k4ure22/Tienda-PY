from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Producto, Usuario
from .forms import ProductoForm, UsuarioForm
import pandas as pd

#USUARIOS

def home(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("productos")
        else:
            return render(request, "core/index.html", {"error": "Credenciales inválidas"})
    return render(request, "core/index.html")

Usuario = get_user_model()

def registro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("perfil_usuario", id=form.instance.id)
    else:
        form = UsuarioForm()
    return render(request, "core/registro.html", {"form": form})


def perfil_usuario(request, email):
    usuario = get_object_or_404(Usuario, email=email)
    return render(request, "core/perfil_usuario.html", {"usuario": usuario})

def logout_usuario(request):
    request.session.flush()  
    return redirect('login') 

# PRODUCTOS
def productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(modelo__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'core/productos.html', {'productos': productos})

def crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        marca = request.POST.get("marca")
        otra_marca = request.POST.get("otra_marca")

        if marca == "Otro" and otra_marca:
            request.POST = request.POST.copy()
            request.POST["marca"] = otra_marca
            form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("productos")
    else:
        form = ProductoForm()

    marcas = Producto.objects.values_list("marca", flat=True).distinct()
    return render(request, "core/crear.html", {"form": form, "marcas": marcas})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "core/detalle_producto.html", {"producto": producto})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("detalle_producto", id=producto.id)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "core/editar_producto.html", {"form": form, "producto": producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect("productos")
    return render(request, "core/eliminar_confirmar.html", {"producto": producto})


def inventario(request):
    return render(request, 'core/inventario.html')

def cargar_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]

        try:
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Producto.objects.create(
                    marca=row.get("marca", ""),
                    modelo=row.get("modelo", ""),
                    almacenamiento=row.get("almacenamiento", ""),
                    ram=row.get("ram", ""),
                    procesador=row.get("procesador", ""),
                    serial=row.get("serial", ""),
                    precio=row.get("precio", 0),
                    color=row.get("color", ""),
                    detalles=row.get("detalles", "")
                )

            messages.success(request, "Productos cargados correctamente desde Excel.")
            return redirect("productos")

        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {e}")

    return render(request, "core/cargar_excel.html")
