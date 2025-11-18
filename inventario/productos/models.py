# Modelos de datos para productos y movimientos de stock
from django.db import models
from django.utils import timezone
import os
import uuid
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_size(image):
    # Valida que la imagen no exceda 5MB
    filesize = image.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"El tamaño maximo permitido es de {megabyte_limit} MB")
    
def get_image_path(instance, filename):
    # Genera ruta única para imágenes
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("productos", filename)

class Producto(models.Model):
    # Modelo para productos del inventario
    nombre = models.CharField("Nombre", max_length=50)
    descripcion = models.CharField("Descripcion", max_length=200)
    precio = models.DecimalField("Precio", max_digits=10, decimal_places=2)  # Precio con 2 decimales
    stock = models.IntegerField(default=0)  # Stock actual
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Minimo")  # Stock mínimo para alertas
    imagen = models.ImageField(
        "Imagen", 
        upload_to=get_image_path, 
        validators=[validate_image_size],  # Validador de tamaño
        blank=True,
        null=True,
        help_text="Formatos permitidos: jpg, png, gif. Tamaño maximo: 5MB"
    )
    fecha_creacion = models.DateTimeField("Fecha de creacion", auto_now_add=True)  # Fecha creación automática
    fecha_actualizacion = models.DateTimeField("Fecha de creacion", auto_now=True)  # Fecha actualización automática
    sku = models.CharField(max_length=50, unique=True)  # Código único del producto

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']  # Orden por defecto por nombre

    def __str__(self):
        return self.nombre  # Representación en string
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagen:
            try:
                # Procesa imagen para redimensionar si es muy grande
                img = Image.open(self.imagen.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.imagen.path)
            except Exception as e:
                print(f"Error al procesar la imagen {e}")

    @property
    def necesita_reposicion(self):
        # Propiedad que indica si el stock está por debajo del mínimo
        return self.stock < self.stock_minimo

class MovimientoStock(models.Model):
    # Modelo para registrar movimientos de stock (entradas, salidas, ajustes)
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("salida", "Salida"), 
        ("ajuste", "Ajuste"),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')  # Relación con producto
    tipo = models.CharField("Tipo", max_length=50, choices=TIPO_CHOICES)  # Tipo de movimiento
    cantidad = models.IntegerField()  # Cantidad movida
    motivo = models.CharField("Motivo", max_length=200, blank=True, null=True)  # Motivo opcional
    fecha = models.DateTimeField("Fecha", default=timezone.now)  # Fecha automática
    usuario = models.CharField("Usuario", max_length=50)  # Usuario que realiza el movimiento

    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ["-fecha"]  # Orden descendente por fecha

    def __str__(self):
        return f"{self.producto.nombre} {self.tipo} {self.cantidad}"  # Representación descriptiva