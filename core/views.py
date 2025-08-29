from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Producto, Usuario, Venta, SolicitudRegistro
from .forms import ProductoForm, UsuarioForm, SolicitudRegistroForm
import pandas as pd
from django.db.models import Q
import unicodedata
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# ======================
# SECCIÓN: USUARIOS
# ======================

def home(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(
                request,
                "core/usuario/inises.html",
                {"error": "Usuario no registrado"}
            )

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect("productos")
            else:
                return redirect("index")
        else:
            return render(
                request,
                "core/usuario/inises.html",
                {"error": "Credenciales inválidas"}
            )
    return render(request, "core/usuario/inises.html")


def registro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) 
            return redirect("perfil_usuario", id=usuario.id)
    else:
        form = UsuarioForm()
    return render(request, "core/usuario/registro.html", {"form": form})

def logout_usuario(request):
    logout(request)
    return redirect('login')

def perfil_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, "core/usuario/perfil_usuario.html", {"usuario": usuario})

def solicitar_registro(request):
    if request.method == "POST":
        form = SolicitudRegistroForm(request.POST)
        if form.is_valid():
            solicitud = form.save()

            # Enviar correo al admin
            asunto = "Nueva Solicitud de Registro"
            mensaje = (
                f"Se ha recibido una nueva solicitud de registro:\n\n"
                f"Nombres: {solicitud.nombres}\n"
                f"Identificación: {solicitud.tipo_identificacion} {solicitud.numero_identificacion}\n"
                f"Edad: {solicitud.edad}\n"
                f"Dirección: {solicitud.direccion}\n"
                f"Correo: {solicitud.correo}\n"
                f"Teléfono: {solicitud.telefono}\n"
                f"Cargo: {solicitud.cargo}\n"
            )
            send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, ["martinmh0722@gmail.com"])

            return render(request, "core/solicitud_exitosa.html")
    else:
        form = SolicitudRegistroForm()
    return render(request, "core/usuario/solicitar_registro.html", {"form": form})
# ======================
# SECCIÓN: CLIENTE
# ======================

def index(request):
    query = request.GET.get("q")
    productos = Producto.objects.all().order_by("marca")

    if query:
        q = normalize_text(query)
        productos = [p for p in productos if
            q in normalize_text(p.marca) or
            q in normalize_text(p.modelo) or
            q in normalize_text(p.almacenamiento) or
            q in normalize_text(p.ram) or
            q in normalize_text(p.procesador) or
            q in normalize_text(p.serial) or
            q in normalize_text(str(p.precio)) or
            q in normalize_text(p.color) or
            q in normalize_text(p.detalles)
        ]

    return render(request, "core/cliente/index.html", {"productos": productos, "query": query})

def detalle_producto_cliente(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "core/cliente/det_prod_cliente.html", {"producto": producto})


def add_to_cart(request, id):
    # lógica de añadir al carrito
    return redirect("index")

def comprar(request, id):
    # lógica de compra inmediata
    return redirect("index")

# ======================
# SECCIÓN: ADMIN PRODUCTOS
# ======================

def productos(request):
    query = request.GET.get("q")
    productos = Producto.objects.all().order_by("marca")

    if query:
        q = normalize_text(query)
        productos = [p for p in productos if
            q in normalize_text(p.marca) or
            q in normalize_text(p.modelo) or
            q in normalize_text(p.almacenamiento) or
            q in normalize_text(p.ram) or
            q in normalize_text(p.procesador) or
            q in normalize_text(p.serial) or
            q in normalize_text(str(p.precio)) or
            q in normalize_text(p.color) or
            q in normalize_text(p.detalles)
        ]

    return render(request, "core/admin/productos.html", {"productos": productos, "query": query})

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
    return render(request, "core/admin/crear.html", {"form": form, "marcas": marcas})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "core/admin/detalle_producto.html", {"producto": producto})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("detalle_producto", id=producto.id)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "core/admin/editar_producto.html", {"form": form, "producto": producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect("productos")
    return render(request, "core/admin/eliminar_confirmar.html", {"producto": producto})

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

    return render(request, "core/admin/cargar_excel.html")


# ======================
# SECCIÓN: FACTURACIÓN
# ======================

def facturar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        cedula = request.POST.get("cedula")
        telefono = request.POST.get("telefono")

        venta = Venta.objects.create(
            producto=producto,
            cliente_nombre=nombre,
            cliente_cedula=cedula,
            cliente_telefono=telefono,
            vendedor=request.user
         )

        return render(request, "core/admin/factura.html", {
            "producto": producto,
            "cliente": {"nombre": nombre, "cedula": cedula, "telefono": telefono},
            "vendedor": request.user
        })

    return render(request, "core/admin/facturar_form.html", {"producto": producto})


# ======================
# UTILIDADES
# ======================

def normalize_text(texto):
    if texto:
        texto = texto.strip()  
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto.lower()
    return ''
