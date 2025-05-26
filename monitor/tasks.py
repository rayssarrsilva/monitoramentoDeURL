from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Url, Notificacao
from .utils import verificar_status 


@shared_task
def verificar_urls():
    for url in Url.objects.filter(receber_notificacoes=True):
        # Verifica se é dia da semana permitido
        hoje = now().strftime('%A').lower()  # exemplo: 'monday'
        dias_permitidos = [d.strip().lower() for d in (url.dias_da_semana or "").split(',')]

        if dias_permitidos and hoje not in dias_permitidos:
            continue

        # Frequência
        if not url.frequencia_minutos:
            continue
        if url.ultimaVerificacao and url.ultimaVerificacao + timedelta(minutes=url.frequencia_minutos) > now():
            continue

        # Verifica status
        status = verificar_status(url.url)
        url.statusAtual = status
        url.ultimaVerificacao = now()
        url.save()

        # 🔔 Cria notificação sempre que checado
        Notificacao.objects.create(
            usuario=url.usuario,
            url=url,
            mensagem=f"A URL {url.url} foi verificada e está: {status}.",
        )

def verificar_uma_url(url_id):
    try:
        url = Url.objects.get(id=url_id)
        status = verificar_status(url.url)
        url.statusAtual = status
        url.ultimaVerificacao = now()
        url.save()

        if status == 'offline':
            Notificacao.objects.create(
                usuario=url.usuario,
                url=url,
                mensagem=f"A URL {url.url} está fora do ar.",
            )
    except Url.DoesNotExist:
        pass
