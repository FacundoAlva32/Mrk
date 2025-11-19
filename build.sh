#!/usr/bin/env bash
set -o errexit

echo "=========================================="
echo "BUILD - MASIVO TECH"
echo "=========================================="

# Limpieza de cache (opcional)
echo "=== CLEANING CACHE ==="
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# =============================================================================
# VERIFICACIONES DE CONFIGURACIÓN
# =============================================================================

echo "=== VERIFICANDO CONFIGURACIÓN ==="

# Verificar PostgreSQL
echo "--- POSTGRESQL CHECK ---"
python -c "
import os
import sys
database_url = os.getenv('DATABASE_URL', '')
if database_url:
    print('✅ DATABASE_URL configurada')
    if 'postgres' in database_url:
        print('✅ PostgreSQL detectado')
    else:
        print('⚠️  Base de datos no es PostgreSQL:', database_url.split('://')[0])
else:
    print('❌ DATABASE_URL no configurada - usando SQLite')
"

# Verificar Cloudinary
echo "--- CLOUDINARY CHECK ---"
python -c "
import os
cloudinary_configured = all([
    os.getenv('CLOUDINARY_CLOUD_NAME'),
    os.getenv('CLOUDINARY_API_KEY'), 
    os.getenv('CLOUDINARY_API_SECRET')
])
print('CLOUDINARY CONFIGURADO:', cloudinary_configured)
if cloudinary_configured:
    print('✅ Cloudinary activo')
else:
    print('⚠️  Cloudinary no configurado - usando archivos locales')
"

# Verificar entorno
echo "--- ENTORNO CHECK ---"
python -c "
import os
debug = os.getenv('DEBUG', 'False').lower() == 'true'
print('DEBUG:', debug)
print('ENTORNO:', 'DESARROLLO' if debug else 'PRODUCCIÓN')
"

# =============================================================================
# BASE DE DATOS
# =============================================================================

# Migraciones de base de datos
echo "=== APLICANDO MIGRACIONES ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Verificar que la base de datos funciona
echo "=== VERIFICANDO BASE DE DATOS ==="
python -c "
import django
django.setup()
from django.db import connection
from django.contrib.auth.models import User

print('🔍 Probando conexión a la base de datos...')
try:
    # Intentar una consulta simple
    user_count = User.objects.count()
    print(f'✅ Conexión exitosa - Usuarios en DB: {user_count}')
    
    # Verificar el motor de base de datos
    db_engine = connection.settings_dict['ENGINE']
    print(f'✅ Motor de base de datos: {db_engine}')
    
    if 'postgres' in db_engine:
        print('✅ PostgreSQL funcionando correctamente')
    else:
        print('⚠️  Usando SQLite (no PostgreSQL)')
        
except Exception as e:
    print(f'❌ Error de base de datos: {e}')
"

# =============================================================================
# ARCHIVOS ESTÁTICOS
# =============================================================================

# Archivos estáticos
echo "=== RECOLECTANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --noinput --clear

# Verificar archivos estáticos recolectados
echo "=== VERIFICANDO ARCHIVOS ESTÁTICOS ==="
python -c "
import os
static_dir = 'staticfiles'
if os.path.exists(static_dir):
    css_files = [f for f in os.listdir(os.path.join(static_dir, 'css')) if f.endswith('.css')] if os.path.exists(os.path.join(static_dir, 'css')) else []
    js_files = [f for f in os.listdir(os.path.join(static_dir, 'js')) if f.endswith('.js')] if os.path.exists(os.path.join(static_dir, 'js')) else []
    print(f'✅ Archivos CSS recolectados: {len(css_files)}')
    print(f'✅ Archivos JS recolectados: {len(js_files)}')
else:
    print('❌ No se encontró directorio staticfiles/')
"

# =============================================================================
# DATOS INICIALES
# =============================================================================

# EJECUTAR SCRIPT DE PRODUCTOS
echo "=== CARGANDO PRODUCTOS ==="
python scripts/load_products.py

# CREAR ADMIN
echo "=== CREANDO ADMIN ==="
python manage.py create_admin

# =============================================================================
# VERIFICACIÓN FINAL
# =============================================================================

echo "=== VERIFICACIÓN FINAL ==="
python -c "
import os
import django
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Product

print('📊 ESTADO FINAL:')
print(f'   👥 Usuarios en sistema: {User.objects.count()}')
print(f'   🎮 Productos cargados: {Product.objects.count()}')
print(f'   ☁️  Cloudinary: {'✅ ACTIVO' if all([os.getenv('CLOUDINARY_CLOUD_NAME'), os.getenv('CLOUDINARY_API_KEY'), os.getenv('CLOUDINARY_API_SECRET')]) else '❌ INACTIVO'}')
print(f'   🗄️  Base de datos: {'✅ POSTGRESQL' if 'postgres' in django.db.connection.settings_dict['ENGINE'] else '⚠️ SQLITE'}')
"

echo "=========================================="
echo "✅ BUILD COMPLETADO EXITOSAMENTE"
echo "=========================================="