
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="inicioSesion"),
    path("login/", views.home, name="login"),
    path("registro/", views.registro, name="registro"),
    path('productos/', views.productos, name='productos'),
    path('inventario/', views.inventario, name='inventario'),
    path('crear/', views.crear, name='crear'),
]
