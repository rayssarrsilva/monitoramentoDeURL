FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /code

# Instala dependências
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . /code/

# Roda comandos importantes de produção
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expõe a porta
EXPOSE 8000

# Inicia o servidor
CMD ["gunicorn", "monitoria.wsgi:application", "--bind", "0.0.0.0:${PORT:-8000}"]
