from django.contrib import admin
from .models import Url, Notificacao, StatusHistorico, HistoricoDeAcesso

# Register your models here.

admin.site.register(Url)
admin.site.register(Notificacao)
admin.site.register(StatusHistorico)
admin.site.register(HistoricoDeAcesso)
