from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Producto,Platillo,Mesa

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            login(request, user)

            if user.username == "bodega02" or user.groups.filter(name='Bodega').exists():
                return redirect('bodega')

            elif user.username == "cocina03" or user.groups.filter(name='Cocina').exists():
                return redirect('cocina')

            elif user.username == "garzon04" or user.groups.filter(name='Garzon').exists():
                return redirect('garzon')

            elif user.username == "caja05" or user.groups.filter(name='Caja').exists():
                return redirect('inicio')

            elif user.username == "administrador01":
                return redirect('administrador')

            else:
                return redirect('inicio')

        else:
            messages.error(request, 'Usuario o contraseña incorrectos')


    return render(request, 'login.html')

@login_required
def inicio(request):
    return render(request, 'inicio.html')

#ADMINISTRADOR
@login_required
def administrador_view(request):
    return render(request, 'administrador.html')

@login_required
def gestion_usuarios_view(request):
    usuarios = User.objects.all()
    return render(request, 'gestion_usuarios.html', {'usuarios': usuarios})

@login_required
def eliminar_usuario_view(request):
    if request.method == "POST":
        user_id = request.POST.get('usuario_id')
        try:
            usuario = User.objects.get(id=user_id)
            usuario.delete()
            messages.success(request, f"Usuario {usuario.username} eliminado correctamente.")
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
    return redirect('gestion_usuarios')

@login_required
def menu_cliente_view(request):
    if request.method == "POST":
        platillo_id = request.POST.get("platillo_id")
        nombre = request.POST.get("nombre")
        ingredientes = request.POST.get("ingredientes")
        precio = request.POST.get("precio")
        imagen = request.FILES.get("imagen")

        if platillo_id:
            platillo = get_object_or_404(Platillo, id=platillo_id)
            platillo.nombre = nombre
            platillo.ingredientes = ingredientes
            platillo.precio = precio
            if imagen:
                platillo.imagen = imagen
            platillo.save()
        else:
            Platillo.objects.create(
                nombre=nombre,
                ingredientes=ingredientes,
                precio=precio,
                imagen=imagen
            )
        return redirect('menu_cliente')

    platillos = Platillo.objects.all()
    return render(request, 'menu_cliente.html', {'platillos': platillos})

@login_required
def eliminar_platillo(request, id):
    if request.method == "POST":
        platillo = get_object_or_404(Platillo, id=id)
        platillo.delete()
    return redirect('menu_cliente')

@login_required
def gestion_mesas(request):
    if request.method == 'POST':
        if 'nueva_mesa' in request.POST:
            numero = request.POST.get('numero')
            if numero:
                Mesa.objects.create(numero=numero, estado='disponible')
        elif 'cambiar_estado' in request.POST:
            mesa_id = request.POST.get('mesa_id')
            mesa = Mesa.objects.get(id=mesa_id)
            mesa.estado = 'no_disponible' if mesa.estado == 'disponible' else 'disponible'
            mesa.save()
        return redirect('gestion_mesas')

    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'gestion_mesas.html', {'mesas': mesas})

def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('gestion_mesas')

#BODEGA
@login_required
def bodega_view(request):

# SOLO USUARIOS DE BODEGA
    if not request.user.groups.filter(name='Bodega').exists() and request.user.username != "bodega02":
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('inicio')

    if request.method == 'POST':
# ELIMINAR PRODUCTO
        if 'eliminar_id' in request.POST:
            producto_id = request.POST.get('eliminar_id')
            producto = get_object_or_404(Producto, id=producto_id)
            producto.delete()
            messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
            return redirect('bodega')

# REGISTRAR MOVIMIENTO
        elif 'tipoMovimiento' in request.POST:
            producto_id = request.POST.get('producto_id')
            tipo = request.POST.get('tipoMovimiento')
            cantidad = request.POST.get('cantidadMovimiento')

            if not (producto_id and tipo and cantidad):
                messages.error(request, "Faltan datos del movimiento.")
                return redirect('bodega')

            producto = get_object_or_404(Producto, id=producto_id)

            try:
                cantidad = int(cantidad)
            except ValueError:
                messages.error(request, "La cantidad debe ser un número.")
                return redirect('bodega')

            if tipo == 'ingreso':
                producto.cantidad += cantidad
                producto.save()
                messages.success(request, f'Se agregaron {cantidad} unidades a "{producto.nombre}".')
            elif tipo == 'salida':
                if cantidad > producto.cantidad:
                    messages.error(request, f"No hay suficiente stock. Stock actual: {producto.cantidad}.")
                    return redirect('bodega')
                producto.cantidad -= cantidad
                producto.save()
                messages.success(request, f'Se retiraron {cantidad} unidades de "{producto.nombre}".')

            return redirect('bodega')

# AGREGAR/EDITAR PRODUCTO
        else:
            producto_id = request.POST.get('producto_id')
            nombre = request.POST.get('nombre')
            proveedor = request.POST.get('proveedor')
            cantidad = request.POST.get('cantidad')
            stock_minimo = request.POST.get('stock_minimo')

            if not (nombre and proveedor and cantidad and stock_minimo):
                messages.error(request, "Por favor completa todos los campos.")
                return redirect('bodega')

            try:
                cantidad = int(cantidad)
                stock_minimo = int(stock_minimo)
            except ValueError:
                messages.error(request, "Los valores numéricos no son válidos.")
                return redirect('bodega')

            if producto_id:
                producto = get_object_or_404(Producto, id=producto_id)
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.cantidad = cantidad
                producto.stock_minimo = stock_minimo
                producto.save()
                messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            else:
                Producto.objects.create(
                    nombre=nombre,
                    proveedor=proveedor,
                    cantidad=cantidad,
                    stock_minimo=stock_minimo
                )
                messages.success(request, f'Producto "{nombre}" agregado exitosamente.')

            return redirect('bodega')

    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'bodega.html', {'productos': productos})

#COCINA
@login_required
def cocina_view(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'cocina.html', {'productos': productos})

#GARZON
@login_required
def garzon_view(request):
    return render(request, 'garzon.html')

#CAJA
@login_required
def caja_view(request):
    return render(request, 'caja.html')

#CLIENTE
@login_required
def cliente_view(request):
    return render(request, 'cliente.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')