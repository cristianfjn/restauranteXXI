from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=20)

    def bajo_stock(self):
        return self.cantidad < self.stock_minimo

    def __str__(self):
        return f"{self.nombre} ({self.proveedor})"
    
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    ingredientes = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Mesa(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No disponible'),
    ]

    numero = models.PositiveIntegerField(unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def __str__(self):
        return f"Mesa {self.numero} ({self.estado})"