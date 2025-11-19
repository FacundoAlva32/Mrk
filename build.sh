#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH - DEBUG COMPLETO"

# Dependencias
pip install -r requirements.txt

# =============================================================================
# DEBUG DETALLADO DE ARCHIVOS ESTÁTICOS
# =============================================================================
echo "=== DEBUG: VERIFICANDO ARCHIVOS EN RENDER ==="

# Verificar estructura del proyecto
echo "1. Estructura del proyecto:"
find . -type d -name "static" -o -name "staticfiles" | sort

echo "2. Contenido de static/ si existe:"
if [ -d "static" ]; then
    echo "✅ static/ EXISTE"
    ls -la static/
    echo "--- CSS files ---"
    find static/ -name "*.css" | head -10
    echo "--- JS files ---" 
    find static/ -name "*.js" | head -10
else
    echo "❌ static/ NO EXISTE"
fi

echo "3. Verificando desde Python:"
python3 -c "
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
static_path = BASE_DIR / 'static'
staticfiles_path = BASE_DIR / 'staticfiles'

print(f'BASE_DIR: {BASE_DIR}')
print(f'static/ existe: {static_path.exists()}')
print(f'staticfiles/ existe: {staticfiles_path.exists()}')

if static_path.exists():
    print('Contenido de static/:')
    for item in static_path.iterdir():
        print(f'  - {item.name}')
        if item.is_dir():
            for subitem in item.iterdir():
                print(f'    - {subitem.name}')
"

# =============================================================================
# MIGRACIONES
# =============================================================================
echo "=== APLICANDO MIGRACIONES ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# =============================================================================
# COLECTAR ESTÁTICOS CON MÁXIMO VERBOSITY
# =============================================================================
echo "=== COLECTANDO ESTÁTICOS ==="
python manage.py collectstatic --noinput --verbosity 3 --clear

# =============================================================================
# VERIFICAR RESULTADO
# =============================================================================
echo "=== VERIFICANDO RESULTADO ==="
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles/ CREADO"
    echo "Contenido de staticfiles/:"
    ls -la staticfiles/
    
    echo "Archivos CSS en staticfiles/:"
    find staticfiles/ -name "*.css" | head -10
    
    echo "Archivos JS en staticfiles/:"
    find staticfiles/ -name "*.js" | head -10
    
    echo "Total de archivos:"
    find staticfiles/ -type f | wc -l
else
    echo "❌ staticfiles/ NO CREADO"
fi

# =============================================================================
# DATOS INICIALES
# =============================================================================
[ -f "scripts/load_products.py" ] && python scripts/load_products.py

echo "✅ BUILD COMPLETADO - DEBUG FINALIZADO"