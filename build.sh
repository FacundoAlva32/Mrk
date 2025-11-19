#!/usr/bin/env bash
set -o errexit

echo "🚀 BUILD MASIVO TECH"

# Dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Archivos estáticos - CON COPIA MANUAL DE RESPUERDO
echo "Configurando archivos estáticos..."
python manage.py collectstatic --noinput || {
    echo "Usando copia manual..."
    mkdir -p staticfiles
    cp -r static/* staticfiles/ 2>/dev/null || true
}

# Crear admin
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin111@masivotech.com', 'goipdwjsgfpodsngosiudingdao!!!!11')
    print('✅ Admin creado')
else:
    print('✅ Admin ya existe')
"

# Cargar productos
python scripts/load_products.py

echo "✅ BUILD COMPLETADO"