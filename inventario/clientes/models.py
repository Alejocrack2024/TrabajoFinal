from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    # Campo para el nombre del cliente
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    # Campo para el apellido del cliente
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    # Número de documento único para cada cliente
    numero_documento = models.CharField(max_length=9, unique=True, verbose_name='Numero_Documento')
    # Email opcional del cliente
    e_mail = models.EmailField(verbose_name='E-mail', blank=True, null=True)
    # Teléfono opcional del cliente
    telefono = models.CharField(max_length=20, blank=True, null=True)
    # Dirección opcional del cliente
    direccion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"  # Nombre singular en admin
        verbose_name_plural = "Clientes"  # Nombre plural en admin
    
    def get_absolute_url(self):
        # Genera URL para ver el detalle de este cliente específico
        return reverse('clientes:cliente_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        # Representación en string del objeto (nombre completo)
        return f"{self.nombre} {self.apellido}"