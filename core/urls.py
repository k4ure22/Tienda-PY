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
    path("registrar_desde_solicitud/<int:solicitud_id>/", views.registrar_desde_solicitud, name="registrar_desde_solicitud"),
    path("rechazar_solicitud/<int:solicitud_id>/", views.rechazar_solicitud, name="rechazar_solicitud"),

    # Cliente
    path("cliente/producto/<int:id>/", views.detalle_producto_cliente, name="det_prod_cliente"),
    path("factura_pdf/<int:producto_id>/", views.factura_pdf, name="factura_pdf"),
    path("productos/cliente/", views.productos_cliente, name="productos_cliente"),


    # Admin - productos 
    path("productos/", views.productos, name="productos"),
    path("crear/", views.crear, name="crear"),
    path("productos/<int:id>/", views.detalle_producto, name="detalle_producto"),
    path("productos/<int:id>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:id>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    path("productos/cargar_excel/", views.cargar_excel, name="cargar_excel"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path("comprar/<int:producto_id>/", views.comprar, name="comprar"),
    path("solicitud/<int:solicitud_id>/revisar/", views.revisar_solicitud_compra, name="revisar_solicitud_compra"),


    # Admin - facturación
    path("facturar/<int:producto_id>/", views.facturar_producto, name="facturar_producto"),

]
