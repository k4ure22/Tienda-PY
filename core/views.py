from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index.html")
        else:
            return render(request, "index.html", {"error":"Credenciales inválidas"})
    return render(request, "core/index.html")



Usuario = get_user_model()

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validar si ya existe el correo
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado")
            return redirect("registro")
        
        # Crear usuario
        usuario = Usuario.objects.create_user(
            username=email,   # Django siempre requiere un username
            nombre=nombre,
            email=email,
            password=password
        )

        messages.success(request, f"Usuario {nombre} registrado con éxito")
        return redirect("login")  # después de registrar redirige al login

    return render(request, "core/registro.html")

def productos(request):
    return render(request, 'core/productos.html')

def inventario(request):
    return render(request, 'core/inventario.html')

def crear(request):
    return render(request, 'core/crear.html')