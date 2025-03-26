web: gunicorn Meets.wsgi:application --workers=100 --timeout 120 --bind 0.0.0.0:$PORT
release: python manage.py migrate --noinput