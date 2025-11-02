from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('administrador/', views.administrador_view, name='administrador'),
    path('administrador/usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    path('administrador/usuarios/eliminar/', views.eliminar_usuario_view, name='eliminar_usuario'),
    path('menu_cliente/', views.menu_cliente_view, name='menu_cliente'),
    path('menu_cliente/eliminar/<int:id>/', views.eliminar_platillo, name='eliminar_platillo'),
    path('gestion/', views.gestion_mesas, name='gestion_mesas'),
    path('mesas/eliminar/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),
    path('bodega/', views.bodega_view, name='bodega'),
    path('cocina/', views.cocina_view, name='cocina'),
    path('garzon/', views.garzon_view, name='garzon'),
    path('caja/', views.caja_view, name='caja'),
    path('cliente/', views.cliente_view, name='cliente'),
    path('logout/', views.logout_view, name='logout'),
]

