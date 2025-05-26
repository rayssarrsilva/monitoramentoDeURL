from django import forms
from .models import Url, DIAS_SEMANA  # DIAS_SEMANA já deve estar no models.py

class UrlForm(forms.ModelForm):
    receber_notificacoes = forms.BooleanField(required=False, label="Receber notificações")
    dias_da_semana = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('0', 'Domingo'),
            ('1', 'Segunda'),
            ('2', 'Terça'),
            ('3', 'Quarta'),
            ('4', 'Quinta'),
            ('5', 'Sexta'),
            ('6', 'Sábado'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Dias da semana para receber notificação"
    )

    class Meta:
        model = Url
        fields = ['url', 'frequencia_minutos', 'receber_notificacoes', 'dias_da_semana']
