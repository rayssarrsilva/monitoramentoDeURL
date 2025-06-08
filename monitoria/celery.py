import os
from celery import Celery

# Define a configuração padrão do Django para o Celery buscar as settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoria.settings')

# Instancia o Celery com o nome do seu projeto
app = Celery('monitoria')

# Lê todas as configurações que começam com 'CELERY_' do settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tasks dentro dos apps registrados
app.autodiscover_tasks()
