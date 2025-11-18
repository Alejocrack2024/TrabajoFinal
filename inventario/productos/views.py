# Vistas para la gestión de productos
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, F
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Producto, MovimientoStock
from .forms import ProductoForm, MovimientoStockForm, AjusteStockForm

# Mixin para permisos de Stock
class StockPermissionMixin(PermissionRequiredMixin):
    # Permite acceso si tiene permisos O pertenece al grupo 'stock de productos'
    def has_permission(self):
        base_permission = super().has_permission()
        es_de_stock = self.request.user.groups.filter(name='stock de productos').exists()
        return base_permission or es_de_stock

# VISTAS PÚBLICAS (todos los usuarios autenticados pueden ver)
class ProductoListView(LoginRequiredMixin, ListView):
    # Muestra lista de productos con paginación y filtro de stock bajo
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "productos"
    paginate_by = 10  # 10 productos por página

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_bajo = self.request.GET.get('stock_bajo')  # Parámetro para filtrar stock bajo
        if stock_bajo:
            queryset = queryset.filter(stock__lt=F("stock_minimo"))  # Filtra stock < stock_minimo
        return queryset.order_by("nombre")  # Ordena por nombre

class ProductoDetailView(LoginRequiredMixin, DetailView):
    # Muestra detalles de un producto específico con últimos movimientos
    model = Producto
    template_name = "productos/producto_detail.html"
    context_object_name = "producto"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movimientos"] = self.object.movimientos.all()[:10]  # Últimos 10 movimientos
        context["form_ajuste"] = AjusteStockForm  # Formulario para ajuste de stock
        return context

class StockBajoListView(LoginRequiredMixin, ListView):
    # Lista especializada solo para productos con stock bajo
    model = Producto
    template_name = "productos/stock_bajo_list.html"
    context_object_name = "productos"

    def get_queryset(self):
        return Producto.objects.filter(stock__lt=F("stock_minimo")).order_by("nombre")

# VISTAS RESTRINGIDAS (solo stock de productos y Administradores)
class ProductoCreateView(LoginRequiredMixin, StockPermissionMixin, CreateView):
    # Vista para crear nuevo producto
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("productos:producto_list")
    permission_required = "productos.add_producto"  # Permiso para agregar productos

    def form_valid(self, form):
        response = super().form_valid(form)
        # Si hay stock inicial, crea movimiento de entrada
        if form.cleaned_data["stock"] > 0:
            MovimientoStock.objects.create(
                producto=self.object,
                tipo="entrada",
                cantidad=form.cleaned_data["stock"],
                motivo="Stock inicial",
                fecha=timezone.now(),
                usuario=self.request.user.username if self.request.user.is_authenticated else "Sistema"
            )
        messages.success(self.request, "Producto creado exitosamente")
        return response

class ProductoUpdateView(LoginRequiredMixin, StockPermissionMixin, UpdateView):
    # Vista para actualizar producto existente
    model = Producto
    template_name = "productos/producto_form.html"
    form_class = ProductoForm
    success_url = reverse_lazy("productos:producto_list")
    permission_required = "productos.change_producto"  # Permiso para modificar productos

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Producto actualizado exitosamente")
        return response

class ProductoDeleteView(LoginRequiredMixin, StockPermissionMixin, DeleteView):
    # Vista para eliminar producto
    model = Producto
    template_name = "productos/producto_confirm_delete.html"
    success_url = reverse_lazy("productos:producto_list")
    permission_required = "productos.delete_producto"  # Permiso para eliminar productos

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado exitosamente")
        return super().delete(request, *args, **kwargs)

class MovimientoStockCreateView(LoginRequiredMixin, StockPermissionMixin, CreateView):
    # Vista para registrar movimientos de stock (entradas/salidas)
    model = MovimientoStock
    template_name = "productos/movimiento_form.html"
    form_class = MovimientoStockForm
    permission_required = "productos.add_movimientostock"  # Permiso para agregar movimientos

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["producto"] = get_object_or_404(Producto, pk=self.kwargs["pk"])  # Pasa producto al formulario
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = get_object_or_404(Producto, pk=self.kwargs["pk"])  # Añade producto al contexto
        return context

    def form_valid(self, form):
        movimiento = form.save(commit=False)  # Crea objeto sin guardar
        movimiento.producto = get_object_or_404(Producto, pk=self.kwargs["pk"])
        movimiento.usuario = self.request.user.username if self.request.user.is_authenticated else "Sistema"

        # Actualiza stock según tipo de movimiento
        if movimiento.tipo == "entrada":
            movimiento.producto.stock += movimiento.cantidad  # Aumenta stock
        elif movimiento.tipo == "salida":
            if movimiento.producto.stock >= movimiento.cantidad:
                movimiento.producto.stock -= movimiento.cantidad  # Disminuye stock
            else:
                form.add_error("cantidad", "No hay stock suficiente")  # Error si no hay suficiente
                return self.form_invalid(form)
        
        movimiento.producto.save()  # Guarda cambios en producto
        movimiento.save()  # Guarda movimiento

        messages.success(self.request, f"Movimiento de stock registrado exitosamente")
        return redirect("productos:producto_detail", pk=movimiento.producto.pk)

class AjusteStockView(LoginRequiredMixin, StockPermissionMixin, FormView):
    # Vista para ajustar stock a un valor específico
    form_class = AjusteStockForm
    template_name = "productos/ajuste_stock_form.html"
    permission_required = "productos.change_producto"  # Permiso para modificar productos

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["producto"] = get_object_or_404(Producto, pk=self.kwargs["pk"])  # Pasa producto al formulario
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = get_object_or_404(Producto, pk=self.kwargs["pk"])  # Añade producto al contexto
        return context

    def form_valid(self, form):
        producto = get_object_or_404(Producto, pk=self.kwargs["pk"])
        nueva_cantidad = form.cleaned_data["cantidad"]
        motivo = form.cleaned_data["motivo"] or "Ajuste de stock"

        diferencia = nueva_cantidad - producto.stock  # Calcula diferencia

        if diferencia != 0:
            # Determina tipo de movimiento según la diferencia
            tipo = "entrada" if diferencia > 0 else "salida" 
            MovimientoStock.objects.create(
                producto=producto,
                tipo=tipo,
                cantidad=abs(diferencia),  # Valor absoluto de la diferencia
                motivo=motivo,
                fecha=timezone.now(),
                usuario=self.request.user.username if self.request.user.is_authenticated else "Sistema"
            )

            producto.stock = nueva_cantidad  # Actualiza stock
            producto.save()

            messages.success(self.request, f"Stock actualizado exitosamente")
        else:
            messages.info(self.request, f"El stock no ha cambiado")  # Mensaje si no hay cambios

        return redirect("productos:producto_detail", pk=producto.pk)