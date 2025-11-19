#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH - ESTÁTICOS FIX"

# Dependencias
pip install -r requirements.txt

# =============================================================================
# VERIFICACIÓN DE ARCHIVOS
# =============================================================================
echo "=== VERIFICANDO ARCHIVOS ESTÁTICOS ==="

echo "1. static/ existe y tiene:"
ls -la static/
echo "--- CSS: ---"
find static/css -name "*.css" | head -10
echo "--- JS: ---" 
find static/js -name "*.js" | head -10

# =============================================================================
# MIGRACIONES
# =============================================================================
echo "=== APLICANDO MIGRACIONES ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# =============================================================================
# SOLUCIÓN: COLECTAR ESTÁTICOS CON CONFIGURACIÓN ESPECÍFICA
# =============================================================================
echo "=== SOLUCIÓN: COLECTANDO ESTÁTICOS ==="

# Opción A: Forzar collectstatic con settings específicos
python -c "
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masivo_tech.settings')
django.setup()

# Ejecutar collectstatic programáticamente
from django.core.management import call_command
call_command('collectstatic', '--noinput', '--verbosity', '2')
"

# Opción B: Si falla A, usar método directo
echo "=== VERIFICANDO RESULTADO ==="
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles/ CREADO"
    find staticfiles/ -name "*.css" | head -5
    find staticfiles/ -name "*.js" | head -5
else
    echo "❌ staticfiles/ NO CREADO - USANDO MÉTODO MANUAL"
    
    # Crear directorio
    mkdir -p staticfiles
    
    # Copiar archivos manualmente
    cp -r static/* staticfiles/ 2>/dev/null || true
    cp -r static/css staticfiles/ 2>/dev/null || true
    cp -r static/js staticfiles/ 2>/dev/null || true
    cp -r static/images staticfiles/ 2>/dev/null || true
    cp -r static/admin staticfiles/ 2>/dev/null || true
    
    echo "✅ Archivos copiados manualmente"
    ls -la staticfiles/
fi

# =============================================================================
# VERIFICACIÓN FINAL
# =============================================================================
echo "=== VERIFICACIÓN FINAL ==="
[ -d "staticfiles/css" ] && echo "✅ CSS en staticfiles/" && ls staticfiles/css/*.css | head -3
[ -d "staticfiles/js" ] && echo "✅ JS en staticfiles/" && ls staticfiles/js/*.js | head -3

# =============================================================================
# DATOS INICIALES
# =============================================================================
[ -f "scripts/load_products.py" ] && python scripts/load_products.py

echo "✅ BUILD COMPLETADO - ESTÁTICOS CONFIGURADOS"