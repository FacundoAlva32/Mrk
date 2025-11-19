#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH"

# Dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Archivos estáticos
python manage.py collectstatic --noinput

# Crear admin si no existe
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@masivotech.com', 'Admin123!')
    print('✅ Admin creado')
else:
    print('✅ Admin ya existe')
"

# Cargar productos
python scripts/load_products.py

echo "✅ BUILD COMPLETADO"