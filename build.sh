#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH - ESTÁTICOS CORREGIDOS"

# Dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Estáticos - CON LIMPIEZA
echo "=== RECOLECTANDO ESTÁTICOS ==="
rm -rf staticfiles/ || true
python manage.py collectstatic --noinput --clear

# Verificar
echo "=== VERIFICANDO ESTÁTICOS ==="
[ -d "staticfiles/css" ] && echo "✅ CSS encontrado" || echo "❌ Sin CSS"
[ -d "staticfiles/js" ] && echo "✅ JS encontrado" || echo "❌ Sin JS"

# Datos
[ -f "scripts/load_products.py" ] && python scripts/load_products.py

echo "✅ BUILD COMPLETADO - Estáticos verificados"