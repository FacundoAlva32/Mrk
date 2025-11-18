# === settings.py - Configuración Django Optimizada para Render ===
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Cargar variables de entorno - DETECCIÓN MEJORADA PARA RENDER
if os.path.exists('.env.local'):
    load_dotenv('.env.local')  # Desarrollo local
    ENVIRONMENT = 'development'
    print("🔄 Entorno: DESARROLLO")
else:
    load_dotenv()  # Producción (Render)
    ENVIRONMENT = 'production'
    print("🚀 Entorno: PRODUCCIÓN (RENDER)")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD - OPTIMIZADA PARA RENDER
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-para-desarrollo')

# Configuración automática por entorno - MEJORADA PARA RENDER
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.1.*']
else:
    # Para Render, DEBUG debe ser False por seguridad
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuración robusta de ALLOWED_HOSTS para Render
    render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_host:
        ALLOWED_HOSTS = [render_host, '.onrender.com', 'localhost', '127.0.0.1']
    else:
        ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# =============================================================================
# CONFIGURACIÓN CLOUDINARY 
# =============================================================================

# Verificar si Cloudinary está configurado
CLOUDINARY_CONFIGURED = all([
    os.getenv('CLOUDINARY_CLOUD_NAME'),
    os.getenv('CLOUDINARY_API_KEY'), 
    os.getenv('CLOUDINARY_API_SECRET')
])

if CLOUDINARY_CONFIGURED:
    # CLOUDINARY CONFIGURADO - cargar e inicializar
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    from cloudinary_storage.storage import MediaCloudinaryStorage
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
        'PREFIX': 'masivo_tech/'  # ← Organización en carpetas
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    print("☁️  Cloudinary configurado")
else:
    # CLOUDINARY NO CONFIGURADO - archivos locales
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    print("📁 Usando archivos locales para desarrollo")

# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================

INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Apps de terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    
    # Apps locales
    'marketplace',
    'users',
    'chat',
]

# Agregar Cloudinary solo si está configurado
if CLOUDINARY_CONFIGURED:
    INSTALLED_APPS = [
        'cloudinary',
        'cloudinary_storage',
    ] + INSTALLED_APPS

# Debug Toolbar solo en desarrollo
if ENVIRONMENT == 'development':
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    # Middleware de CORS (primero)
    'corsheaders.middleware.CorsMiddleware',
    
    # Middleware de seguridad
    'django.middleware.security.SecurityMiddleware',
    
    # Whitenoise para archivos estáticos en producción -> RENDER
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Middleware de sesión
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Middleware común
    'django.middleware.common.CommonMiddleware',
    
    # Middleware CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Middleware de autenticación
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Middleware de mensajes
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Middleware de clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Middleware de Allauth
    'allauth.account.middleware.AccountMiddleware',
]

# Debug Toolbar solo en desarrollo
if ENVIRONMENT == 'development':
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'masivo_tech.urls'

WSGI_APPLICATION = 'masivo_tech.wsgi.application'

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS - MEJORADA PARA RENDER
# =============================================================================

# Configuración robusta con fallback a SQLite
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    try:
        # PostgreSQL en producción (Render)
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=True
            )
        }
        print("🗄️  Base de datos: PostgreSQL (Render)")
    except Exception as e:
        print(f"❌ Error con PostgreSQL, usando SQLite: {e}")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # SQLite en desarrollo
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("🗄️  Base de datos: SQLite (Desarrollo)")

# =============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# =============================================================================

# Backends de autenticación
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'users.CustomUser'

# Configuración de Allauth
SITE_ID = 1  # CORREGIDO - estaba SIDE_ID
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_STORE_TOKENS = True

# Configuración de protocolo según entorno
if ENVIRONMENT == 'development':
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Configuración de registro
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# =============================================================================
# CONFIGURACIÓN DE EMAIL (OPTIMIZADA PARA RENDER)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = "no-reply@masivotech.com"

# =============================================================================
# CONFIGURACIÓN DE INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA - OPTIMIZADA RENDER
# =============================================================================

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de WhiteNoise para Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos media (configuración local como respaldo)
if not CLOUDINARY_CONFIGURED:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CONFIGURACIÓN DE TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'marketplace.context_processors.cart_context',
            ],
        },
    },
]

# =============================================================================
# CONFIGURACIÓN DE CRISPY FORMS
# =============================================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =============================================================================
# CONFIGURACIÓN DE CARRITO
# =============================================================================

CART_SESSION_ID = 'cart'

# =============================================================================
# CONFIGURACIÓN DE APIs EXTERNAS
# =============================================================================

# Google Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY')

# Google OAuth - SOLO UN ADAPTER
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# USAR SOLO UN ADAPTER - elige uno:
# SOCIALACCOUNT_ADAPTER = 'marketplace.patches.FixedSocialAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD ADICIONAL
# =============================================================================

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de seguridad para producción
if ENVIRONMENT == 'production':
    # Security settings para producción
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# URL base para callbacks
BASE_URL = os.getenv("BASE_URL", "https://masivotest.onrender.com")

# Configuración del admin dashboard
ADMIN_DASHBOARD = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración Debug Toolbar para desarrollo
if ENVIRONMENT == 'development':
    INTERNAL_IPS = ['127.0.0.1']

# =============================================================================
# LOGGING PARA RENDER - PARA VER ERRORES EN PRODUCCIÓN
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

print("✅ Settings cargado correctamente")
print(f"📍 ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"🔧 DEBUG: {DEBUG}")
print(f"☁️  CLOUDINARY: {CLOUDINARY_CONFIGURED}")
print(f"🗄️  DATABASE: {DATABASES['default']['ENGINE']}")