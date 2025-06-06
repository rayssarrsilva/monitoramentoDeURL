FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

WORKDIR /code/monitoria  

EXPOSE 8000

CMD bash -c " python manage.py migrate && python manage.py collectstatic --noinput &&gunicorn monitoria.wsgi:application --bind 0.0.0.0:${PORT}"
