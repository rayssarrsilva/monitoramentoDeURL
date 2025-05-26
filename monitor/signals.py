from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Url
import json

@receiver(post_save, sender=Url)
def criar_tarefa_periodica(sender, instance, **kwargs):
    if not instance.frequencia_minutos:
        return  # Não cria nada se a frequência não estiver definida

    # Cria ou pega o intervalo
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=instance.frequencia_minutos,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name=f"Verificar URL {instance.id}",
        defaults={
            'interval': schedule,
            'task': 'monitor.tasks.verificar_uma_url',
            'args': json.dumps([instance.id])
        }
    )
