FROM python:3.11-slim

WORKDIR /code

# Instala dependências
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . /code/

# Copia e configura o entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

COPY start_worker.sh /start_worker.sh
RUN chmod +x /start_worker.sh

COPY start_beat.sh /start_beat.sh
RUN chmod +x /start_beat.sh

# Usa o entrypoint customizado
ENTRYPOINT ["/entrypoint.sh"]
