from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Url, Notificacao
from .utils import verificar_status 

@shared_task
def verificar_urls():
    dia_map = {
        'monday': 'seg', 'tuesday': 'ter', 'wednesday': 'qua', 'thursday': 'qui',
        'friday': 'sex', 'saturday': 'sab', 'sunday': 'dom'
    }
    hoje = dia_map.get(now().strftime('%A').lower(), '')

    for url in Url.objects.filter(receber_notificacoes=True):
        dias_permitidos = [d.strip() for d in (url.dias_da_semana or "").split(',')]

        if dias_permitidos and hoje not in dias_permitidos:
            continue

        if not url.frequencia_minutos:
            continue
        if url.ultimaVerificacao and url.ultimaVerificacao + timedelta(minutes=url.frequencia_minutos) > now():
            continue

        status = verificar_status(url.url)
        url.statusAtual = status
        url.ultimaVerificacao = now()
        url.save()

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
