from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth import logout

# Vista personalizada para logout
def custom_logout(request):
    """Logout personalizado que redirige a la lista de productos en lugar del admin"""
    logout(request)  # Cierra la sesión del usuario
    return redirect('productos:producto_list')  # Redirige a la lista de productos

# Patrones de URL del proyecto
urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # URLs de productos en la raíz del sitio
    path("", include("productos.urls")),
    
    # URLs de clientes con prefijo /clientes/
    path('clientes/', include("clientes.urls")),
    
    # URLs de ventas con prefijo /ventas/
    path('ventas/', include("ventas.urls")),
    
    # URLs de autenticación de allauth
    path('accounts/', include('allauth.urls')),
    
    # Vista de login personalizada
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',  # Template personalizado
        redirect_authenticated_user=True          # Redirige usuarios ya autenticados
    ), name='login'),
    
    # Vista de logout personalizada
    path('accounts/logout/', custom_logout, name='custom_logout'),
]

# En modo desarrollo, servir archivos de media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)