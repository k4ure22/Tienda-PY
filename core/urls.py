
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="inicioSesion"),
    path("login/", views.home, name="login"),
    path("registro/", views.registro, name="registro"),
    path("perfil_usuario/<str:email>/", views.perfil_usuario, name="perfil_usuario"),
    path('logout/', views.logout_usuario, name='logout'),
    path('crear/', views.crear, name='crear'),
    path('productos/', views.productos, name='productos'),
    path("productos/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path("productos/<int:id>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    path('inventario/', views.inventario, name='inventario'),
    path("productos/cargar_excel/", views.cargar_excel, name="cargar_excel"),
]
