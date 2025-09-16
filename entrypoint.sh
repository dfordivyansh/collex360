#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Create superuser if none exists
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
        os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
        os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
    )
"

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn collex360.wsgi:application --bind 0.0.0.0:8000
