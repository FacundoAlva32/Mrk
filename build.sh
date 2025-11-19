#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH"

pip install -r requirements.txt

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Estáticos - limpio y simple
python manage.py collectstatic --noinput --clear

python scripts/load_products.py

echo "✅ BUILD COMPLETADO"