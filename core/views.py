from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Producto, Usuario, Venta, SolicitudRegistro, SolicitudCompra
from .forms import ProductoForm, UsuarioForm, SolicitudRegistroForm, SolicitudCompraForm
import pandas as pd
from django.db.models import Q 
import unicodedata 
from django.core.mail import send_mail 
from django.conf import settings 
from django.template.loader import get_template 
from xhtml2pdf import pisa  
from django.utils.crypto import get_random_string 


User = get_user_model()

# ======================
# SECCIÓN: USUARIOS
# ======================
def home(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.cargo == "admin":
                return redirect("productos")  # vista de admin
            else:
                return redirect("productos_cliente")  # vista de cliente
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
            usuario = form.save(commit=False)
            cargo = form.cleaned_data.get("cargo")

            if cargo == "admin":
                return render(request, "core/usuario/solicitar_registro.html", {"form": form})
            else:
                usuario.save()
                login(request, usuario)
                return redirect("productos_cliente")
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

            return render(request, "core/usuario/solicitud_exitosa.html")
    else:
        form = SolicitudRegistroForm()
    return render(request, "core/usuario/solicitar_registro.html", {"form": form})

@login_required
def solicitudes(request):
    solicitudes_registro = SolicitudRegistro.objects.all().order_by("-id")  
    solicitudes_compra = Venta.objects.all().order_by("-id")

    return render(request, "core/admin/solicitudes.html", {
        "solicitudes_registro": solicitudes_registro,
        "solicitudes_compra": solicitudes_compra,
    })

@login_required
def registrar_desde_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudRegistro, id=solicitud_id)

    
    password = get_random_string(8)

    usuario = Usuario.objects.create_user(
        username=solicitud.correo,
        password=password,
        nombre=solicitud.nombres,
        email=solicitud.correo,
        telefono=solicitud.telefono,
        direccion=solicitud.direccion,
        cargo=solicitud.cargo,
    )

   
    solicitud.delete()

    
    send_mail(
        "Registro aprobado",
        f"Hola {usuario.nombre}, tu registro fue aprobado.\n\n"
        f"Usuario: {usuario.username}\nContraseña: {password}\n\n"
        f"Por favor cambia tu contraseña al iniciar sesión.",
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
    )

    messages.success(request, f"Se registró a {usuario.nombre} y se envió su contraseña al correo.")
    return redirect("solicitudes")

@login_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudRegistro, id=solicitud_id)

    if request.method == "POST":
        solicitud.delete()
        messages.success(request, "La solicitud ha sido rechazada correctamente.")
        return redirect("solicitudes")

    return render(request, "core/admin/rechazar_confirmar.html", {"solicitud": solicitud})
@login_required
def perfil_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        if "eliminar" in request.POST:
            usuario.delete()
            messages.success(request, "Tu cuenta ha sido eliminada.")
            return redirect("login")

        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            # Si no quiere cambiar contraseña, no la sobreescribimos
            if not form.cleaned_data["password"]:
                form.instance.password = usuario.password
            else:
                form.instance.set_password(form.cleaned_data["password"])
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil_usuario", id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, "core/usuario/perfil_usuario.html", {
        "usuario": usuario,
        "form": form
    })

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


def productos_cliente(request):
    query = request.GET.get("q")
    productos = Producto.objects.all().order_by("marca")

    if query:
        q = normalize_text(query)
        productos = [
            p for p in productos if
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

    return render(request, "core/cliente/productos_cliente.html", {"productos": productos})


def detalle_producto_cliente(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "core/cliente/det_prod_cliente.html", {"producto": producto})





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
            print(df.head())

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

def comprar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)  # ✅ usar producto_id

    if request.method == "POST":
        form = SolicitudCompraForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.producto = producto 
            solicitud.save()

            # Enviar correo al admin
            asunto = f"Nueva solicitud de compra: {producto.marca} {producto.modelo}"
            mensaje = (
                f"Se ha registrado una solicitud de compra.\n\n"
                f"Cliente: {solicitud.cliente_nombre}\n"
                f"Cédula: {solicitud.cliente_cedula}\n"
                f"Teléfono: {solicitud.cliente_telefono}\n"
                f"Dirección: {solicitud.cliente_direccion}\n"
                f"Correo: {solicitud.cliente_correo}\n"
                f"Producto: {producto.marca} {producto.modelo}\n"
                f"Precio: ${producto.precio}\n"
            )
            send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, ["martin102230@gmail.com"])

            return redirect("solicitudes")  # o donde quieras redirigir
    else:
        form = SolicitudCompraForm()

    return render(request, "core/cliente/solicitud_compra.html", {"form": form, "producto": producto})


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


def factura_pdf(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedor = request.user

    # ⚡ Cliente desde la última venta de este producto
    venta = Venta.objects.filter(producto=producto).last()
    cliente = {
        "nombre": venta.cliente_nombre if venta else "N/A",
        "cedula": venta.cliente_cedula if venta else "N/A",
        "telefono": venta.cliente_telefono if venta else "N/A"
    }

    template_path = "core/admin/factura.html"
    context = {
        "producto": producto,
        "cliente": cliente,
        "vendedor": vendedor
    }

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="factura_{producto.modelo}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)

    return response



def revisar_solicitud_compra(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCompra, id=solicitud_id)
    return render(request, "core/admin/revisar_solicitud.html", {"solicitud": solicitud})

# ======================
# UTILIDADES
# ======================

def normalize_text(texto):
    if texto:
        texto = texto.strip()  
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto.lower()
    return ''


