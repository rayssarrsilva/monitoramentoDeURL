from django.db import models
from django.contrib.auth.models import User # modelo padrao django, associado a quem cadastrou a URL
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

# Create your models here.

DIAS_SEMANA = [
    ('seg', 'Segunda'),
    ('ter', 'Terça'),
    ('qua', 'Quarta'),
    ('qui', 'Quinta'),
    ('sex', 'Sexta'),
    ('sab', 'Sábado'),
    ('dom', 'Domingo'),
]

class Url(models.Model): #torna um model
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #deleta em cascade tudo que estiver relacionado ao user
    url = models.URLField()
    statusAtual = models.CharField(max_length=50, default='desconhecido')
    ultimaVerificacao = models.DateTimeField(null=True, blank=True)
    DataCriacao = models.DateField(auto_now_add=True) # armazena automaticamente a data/hora
    frequencia_minutos = models.IntegerField(null=True, blank=True)
    receber_notificacoes = models.BooleanField(default=False)
    dias_da_semana = models.CharField(max_length=100, blank=True)  # Ex: "seg,qua,sex"

    def __str__(self):
        return self.url
    
    class Meta:
        unique_together = ('usuario', 'url')

    
class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    mensagem = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario} sobre {self.url.url}"
    
class StatusHistorico(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)

class HistoricoDeAcesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='HistoricoDeAcesso')
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='acessos')
    status = models.CharField(max_length=30)  # <-- adicione isso
    data = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Url)
def criar_ou_remover_task(sender, instance, **kwargs):
    nome_tarefa = f"verificar_url_{instance.id}"

    if not instance.frequencia_minutos:
        # Remove a tarefa se existir
        PeriodicTask.objects.filter(name=nome_tarefa).delete()
        return

    # Cria ou atualiza o intervalo
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=instance.frequencia_minutos,
        period=IntervalSchedule.MINUTES
    )

    # Cria ou atualiza a tarefa
    PeriodicTask.objects.update_or_create(
        name=nome_tarefa,
        defaults={
            'interval': schedule,
            'task': 'monitor.tasks.verificar_urls',
            'args': json.dumps([]),
        }
    )

@receiver(post_save, sender=Url)
def criar_ou_remover_task(sender, instance, **kwargs):
    nome_tarefa = f"verificar_url_{instance.id}"

    # Só cria se o usuário ativou
    if not instance.receber_notificacoes or not instance.frequencia_minutos:
        PeriodicTask.objects.filter(name=nome_tarefa).delete()
        return

    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=instance.frequencia_minutos,
        period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.update_or_create(
        name=nome_tarefa,
        defaults={
            'interval': schedule,
            'task': 'monitor.tasks.verificar_urls',
            'args': json.dumps([]),
        }
    )
