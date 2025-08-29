from django.urls import path
from . import views

urlpatterns = [
    # Página principal → catálogo (cliente)
    path("", views.index, name="index"),

    # Usuario (solo admin/empleado)
    path("inises/", views.home, name="login"),
    path("registro/", views.registro, name="registro"),
    path("perfil_usuario/<int:id>/", views.perfil_usuario, name="perfil_usuario"),
    path("logout/", views.logout_usuario, name="logout"),
    path("solicitar_registro/", views.solicitar_registro, name="solicitar_registro"),

    # Cliente
    path("carrito/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("comprar/<int:id>/", views.comprar, name="comprar"),
    path("cliente/producto/<int:id>/", views.detalle_producto_cliente, name="det_prod_cliente"),

    # Admin - productos 
    path("productos/", views.productos, name="productos"),
    path("crear/", views.crear, name="crear"),
    path("productos/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path("productos/<int:id>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    path("productos/cargar_excel/", views.cargar_excel, name="cargar_excel"),

    # Admin - facturación
    path("facturar/<int:producto_id>/", views.facturar_producto, name="facturar_producto"),
]
