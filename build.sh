#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH"

pip install -r requirements.txt

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Cargar datos desde SQLite (si el archivo existe)
if [ -f "datos.json" ]; then
    python manage.py loaddata datos.json
    echo "✅ Datos migrados desde SQLite"
    rm datos.json  # Limpiar después de cargar
fi

python manage.py collectstatic --noinput

python scripts/load_products.py

echo "✅ BUILD COMPLETADO"