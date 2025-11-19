# === settings.py - Configuración Django Optimizada ===
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Cargar variables de entorno
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-para-desarrollo')

# Detección automática de entorno
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.onrender.com', 'localhost', '127.0.0.1']
else:
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# =============================================================================
# CONFIGURACIÓN CLOUDINARY 
# =============================================================================

CLOUDINARY_CONFIGURED = all([
    os.getenv('CLOUDINARY_CLOUD_NAME'),
    os.getenv('CLOUDINARY_API_KEY'), 
    os.getenv('CLOUDINARY_API_SECRET')
])

if CLOUDINARY_CONFIGURED:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    from cloudinary_storage.storage import MediaCloudinaryStorage
    
    cloudinary.config( 
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'), 
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    
    'marketplace',
    'users',
    'chat',
]

if CLOUDINARY_CONFIGURED:
    INSTALLED_APPS = ['cloudinary', 'cloudinary_storage'] + INSTALLED_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'masivo_tech.urls'
WSGI_APPLICATION = 'masivo_tech.wsgi.application'

# =============================================================================
# BASE DE DATOS
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

# =============================================================================
# AUTENTICACIÓN
# =============================================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = 'users.CustomUser'
SITE_ID = 1
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

if RENDER_EXTERNAL_HOSTNAME:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# =============================================================================
# ARCHIVOS ESTÁTICOS - SOLUCIÓN DEFINITIVA
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ SOLUCIÓN: WhiteNoise con configuración correcta
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# Configuración adicional para WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# =============================================================================
# TEMPLATES Y OTRAS CONFIGURACIONES
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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CART_SESSION_ID = 'cart'

# APIs
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID',''), 
            'secret': os.getenv('GOOGLE_SECRET', ''),    
            'key': ''
        }
    }
}
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

# Seguridad
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
BASE_URL = os.getenv("BASE_URL", "https://masivotest.onrender.com")
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de seguridad para producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

print("✅ Settings cargado - Configuración optimizada para Render")