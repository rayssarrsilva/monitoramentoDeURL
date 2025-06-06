FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

WORKDIR /code/monitoria  

ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "gunicorn monitoria.wsgi:application --bind 0.0.0.0:$PORT"]

