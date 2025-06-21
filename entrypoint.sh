#!/bin/sh

# Aplica as migrações e coleta os arquivos estáticos
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Inicia o servidor
exec gunicorn monitoria.wsgi:application --bind 0.0.0.0:${PORT:-8000}
