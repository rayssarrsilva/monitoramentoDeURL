FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# Copia o entrypoint
COPY entrypoint.sh /entrypoint.sh

# Torna executável (importante pro Render)
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Usa o entrypoint para rodar tudo corretamente
ENTRYPOINT ["/entrypoint.sh"]
