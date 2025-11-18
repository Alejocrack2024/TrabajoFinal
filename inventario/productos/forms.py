# Formularios para la gestión de productos y movimientos de stock
from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, MovimientoStock
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Reset, ButtonHolder, Field, Div, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .crispy import BaseFormHelper

class ProductoForm(forms.ModelForm):
    # Formulario para crear y editar productos
    class Meta:
        model = Producto  # Vincula al modelo Producto
        fields = ["nombre", "sku", "descripcion", "stock", "stock_minimo", "precio", "imagen"]  # Campos incluidos
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),  # Área de texto más grande
        }
        labels = {
            "stock_minimo": "Stock Mínimo (alerta)",  # Etiqueta personalizada
        }
        help_texts = {
            "stock_minimo": "Se mostrará una alerta cuando el stock esté por debajo de ese valor"  # Texto de ayuda
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()  # Helper base para diseño
        self.helper.layout = Layout(
            Field("nombre"),  # Campo estándar
            Field("descripcion"),
            PrependedText("precio", "$", placeholder="0.00"),  # Campo con prefijo $
            Field("stock"),
            Field("stock_minimo"),
            Field("imagen"),
            ButtonHolder(  # Contenedor para botones
                Submit("submit", "Guardar", css_class="btn btn-success"),  # Botón enviar
                Reset("reset", "Limpiar", css_class="btn btn-outline-secondary"),  # Botón limpiar
                HTML('<a href="{% url "productos:producto_list" %}" class="btn btn-secondary">Cancelar</a>')  # Enlace cancelar
            )
        )
    
    def clean_precio(self):
        # Validación: precio debe ser mayor a cero
        precio = self.cleaned_data.get("precio")
        if precio and precio <= 0:
            raise ValidationError("El precio debe ser mayor a cero")
        return precio
    
    def clean_stock(self):
        # Validación: stock no puede ser negativo
        stock = self.cleaned_data.get("stock")
        if stock and stock < 0:
            raise ValidationError("No puede haber valor negativo de stock")
        return stock
    
    def clean_stock_minimo(self):
        # Validación: stock mínimo no puede ser negativo
        stock_minimo = self.cleaned_data.get("stock_minimo")
        if stock_minimo and stock_minimo < 0:
            raise ValidationError("No puede haber valor negativo de stock minimo")
        return stock_minimo

class MovimientoStockForm(forms.ModelForm):
    # Formulario para registrar movimientos de stock (entradas/salidas)
    class Meta:
        model = MovimientoStock
        fields = ["tipo", "cantidad", "motivo"]  # Campos del movimiento
        widgets = {
            "motivo": forms.Textarea(attrs={"rows": 3}),  # Área de texto para motivo
        }
        labels = {
            "tipo": "Tipo de movimiento",
            "cantidad": "Cantidad", 
            "motivo": "Motivo (opcional)"
        }
        
    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop("producto", None)  # Obtiene producto para validaciones
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        
        # Información del producto para contexto
        stock_info = ""
        if self.producto:
            stock_info = f"""
            <div class="alert alert-info">
                <strong>Producto:</strong> {self.producto.nombre}<br>
                <strong>Stock actual:</strong> {self.producto.stock}
            </div>
            """

        self.helper.layout = Layout(
            HTML(stock_info),  # Muestra info del producto
            Field("tipo"),
            Field("cantidad"),
            Field("motivo"),
            ButtonHolder(
                Submit("submit", "Registrar movimiento", css_class="btn btn-success"),
                HTML('<a href="{{ request.META.HTTP_REFERER }}" class="btn btn-secondary">Cancelar</a>')
            )
        )

    def clean_cantidad(self):
        # Validación: cantidad debe ser positiva y suficiente para salidas
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero")
        
        if self.producto and self.cleaned_data.get("tipo") == "salida":
            if cantidad > self.producto.stock:
                raise ValidationError(
                    f"No hay suficiente stock. Disponible: {self.producto.stock}"
                )
        return cantidad

class AjusteStockForm(forms.Form):
    # Formulario para ajustar stock a un valor específico (no basado en modelo)
    cantidad = forms.IntegerField(
        min_value=0,  # Valor mínimo 0
        label="Nuevo Stock",
        help_text="Establece el nuevo valor de stock para el producto."
    )
    motivo = forms.CharField(
        required=False,  # Campo opcional
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Motivo del Ajuste", 
        help_text="Explica por qué estás ajustando el stock (opcional)."
    )

    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        
        # Muestra información actual del producto
        stock_info = ""
        if self.producto:
            stock_info = f"""
            <div class="alert alert-info">
                <strong>Producto:</strong> {self.producto.nombre}<br>
                <strong>Stock actual:</strong> {self.producto.stock}
            </div>
            """
            self.fields['cantidad'].initial = self.producto.stock  # Valor inicial = stock actual
        
        self.helper.layout = Layout(
            HTML(stock_info),
            Field('cantidad'),
            Field('motivo'),
            ButtonHolder(
                Submit('submit', 'Ajustar Stock', css_class='btn btn-warning'),  # Botón amarillo para advertencia
                HTML('<a href="{{ request.META.HTTP_REFERER }}" class="btn btn-secondary">Cancelar</a>')
            )
        )

class FiltroFormHelper(FormHelper):
    # Helper específico para formularios de filtro (método GET)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'get'  # Los filtros usan GET
        self.form_class = 'form-inline'  # Formulario en línea
        self.field_template = 'bootstrap4/layout/inline_field.html'  # Template para campos en línea

class FiltroProductosForm(forms.Form):
    # Formulario para filtrar productos en la lista
    TIPO_FILTRO_CHOICES = [
        ('', 'Todos los productos'),
        ('stock_bajo', 'Solo stock bajo'),
        ('stock_ok', 'Stock normal'),
    ]
    
    filtro = forms.ChoiceField(
        choices=TIPO_FILTRO_CHOICES,
        required=False,  # Campo opcional
        label="Filtrar por"
    )
    buscar = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre, descripción...'})  # Placeholder para búsqueda
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FiltroFormHelper()  # Helper de filtro
        
        # Layout con filas y columnas para diseño responsive
        self.helper.layout = Layout(
            Row(
                Column('filtro', css_class='form-group col-md-4 mb-0'),
                Column('buscar', css_class='form-group col-md-4 mb-0'),
                Column(
                    ButtonHolder(
                        Submit('submit', 'Filtrar', css_class='btn btn-primary'),
                        HTML('<a href="." class="btn btn-secondary">Limpiar</a>')  # Enlace para resetear filtros
                    ),
                    css_class='form-group col-md-4 mb-0'
                ),
                css_class='form-row align-items-center'  # Alineación vertical centrada
            )
        )