"""
Configuración de Django para el proyecto inventario.
Generado por 'django-admin startproject' usando Django 5.2.6.
"""

import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de templates
TEMPLATES = [
    {
        # ... (otras configuraciones)
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directorio global de templates
        # ... (otras configuraciones)
    },
]

# Clave secreta para seguridad - obtenida de variables de entorno
SECRET_KEY = os.environ.get("SECRET_KEY") 

# Modo debug - True para desarrollo
DEBUG = True

# Hosts permitidos - separados por comas desde variables de entorno
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Configuración de autenticación
LOGIN_URL = '/accounts/login/'  # URL para login
LOGIN_REDIRECT_URL = '/'  # Redirigir al home después del login
LOGOUT_REDIRECT_URL = '/'  # Redirigir al home después del logout

# Aplicaciones instaladas
INSTALLED_APPS = [
    # Apps de Django por defecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de terceros
    'bootstrap4',  # Framework CSS Bootstrap 4
    'crispy_forms',  # Formularios estilizados
    'crispy_bootstrap4',  # Integración con Bootstrap 4
    
    # Apps locales del proyecto
    'productos',  # Gestión de productos
    'clientes',    # Gestión de clientes
    'ventas',      # Gestión de ventas
    
    # Apps de autenticación
    'allauth',      # Autenticación avanzada
    'allauth.account',  # Gestión de cuentas
]

# Middleware - procesadores de solicitudes
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sesiones
    'django.middleware.common.CommonMiddleware',  # Funcionalidades comunes
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protección clickjacking
    "allauth.account.middleware.AccountMiddleware",  # Middleware de allauth
]

# Configuración de URLs principal
ROOT_URLCONF = 'inventario.urls'

# Configuración detallada de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor de templates
        'DIRS': [BASE_DIR / 'templates'],  # Directorios adicionales de templates
        'APP_DIRS': True,  # Buscar templates en cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Contexto de request
                'django.contrib.auth.context_processors.auth',  # Contexto de autenticación
                'django.contrib.messages.context_processors.messages',  # Contexto de mensajes
            ],
        },
    },
]

# Aplicación WSGI
WSGI_APPLICATION = 'inventario.wsgi.application'

# Configuración de base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Motor de base de datos
        'NAME': os.environ.get("POSTGRES_DB"),      # Nombre de la base de datos
        'USER': os.environ.get("POSTGRES_USER"),    # Usuario de la base de datos
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),  # Contraseña
        'HOST': os.environ.get("POSTGRES_HOST"),    # Host de la base de datos
        'PORT': os.environ.get("POSTGRES_PORT")     # Puerto
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # No similar a información del usuario
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Longitud mínima
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # No contraseñas comunes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # No solo números
    },
]

# Internacionalización
LANGUAGE_CODE = 'es-ar'  # Idioma español argentina
TIME_ZONE = 'UTC'        # Zona horaria UTC
USE_I18N = True          # Habilitar internacionalización
USE_TZ = True            # Usar zona horaria

# Archivos estáticos y media
STATIC_URL = 'static/'  # URL base para archivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directorios de archivos estáticos
MEDIA_URL = 'media/'    # URL base para archivos de media
MEDIA_ROOT = BASE_DIR / 'media'  # Directorio raíz para archivos subidos

# Campo automático por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'  # Template packs permitidos
CRISPY_TEMPLATE_PACK = 'bootstrap4'           # Template pack por defecto

# Configuración de Bootstrap4
BOOTSTRAP4 = {
    'include_jquery' : True,           # Incluir jQuery automáticamente
    'set_placeholder' : False,         # No establecer placeholders automáticamente
    'required_css_class' : 'required', # Clase CSS para campos requeridos
    'error_css_class' : 'is-invalid',  # Clase CSS para errores
    'success_css_class': 'is-valid',   # Clase CSS para éxito
}

# Backends de autenticación
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',  # Backend de allauth
    'django.contrib.auth.backends.ModelBackend',            # Backend por defecto de Django
]

# Configuración de redirección después de login
LOGIN_REDIRECT_URL = '/'

# Configuración de verificación de email
# 'mandatory' = obligatorio, 'optional' = opcional
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/productos/'    # Redirigir a productos después del login
LOGOUT_REDIRECT_URL = '/accounts/login/'  # Redirigir a login después del logout

# Configuración de métodos de login y registro
ACCOUNT_LOGIN_METHODS = {'username'}  # Método de login solo con username
ACCOUNT_SIGNUP_FIELDS = ['email', 'username*', 'password1*', 'password2*']  # Campos para registro
ACCOUNT_LOGOUT_REDIRECT_URL = '/'     # URL después del logout

# Configuraciones de seguridad y registro
ACCOUNT_ALLOW_REGISTRATION = False   # Desactiva registro de nuevos usuarios
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Sin verificación de email requerida