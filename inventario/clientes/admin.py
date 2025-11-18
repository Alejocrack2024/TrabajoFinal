# clientes/admin.py
from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)  # Registra el modelo Cliente en el admin de Django
class ClienteAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de clientes en el admin
    list_display = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']
    
    # Filtros que aparecerán en la barra lateral (en este caso solo por nombre)
    list_filter = ['nombre']
    
    # Campos por los que se puede buscar en la barra de búsqueda
    search_fields = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']