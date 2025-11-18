# URLs para la aplicación de productos
from django.urls import path
from . import views

app_name = 'productos'  # Namespace para URLs

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto_list'),  # Lista de productos
    path('nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),  # Crear producto
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),  # Detalle producto
    path('<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),  # Editar producto
    path('<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),  # Eliminar producto
    path('<int:pk>/movimiento/', views.MovimientoStockCreateView.as_view(), name='movimiento_create'),  # Registrar movimiento
    path('<int:pk>/ajustar-stock/', views.AjusteStockView.as_view(), name='ajustar_stock'),  # Ajustar stock
    path('stock-bajo/', views.StockBajoListView.as_view(), name='stock_bajo_list'),  # Lista stock bajo
]