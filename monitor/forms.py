from django import forms
from .models import Url, DIAS_SEMANA  # Usa os códigos corretos: 'seg', 'ter', etc.

class UrlForm(forms.ModelForm):
    receber_notificacoes = forms.BooleanField(
        required=False,
        label="Receber notificações"
    )
    
    dias_da_semana = forms.MultipleChoiceField(
        required=False,
        choices=DIAS_SEMANA,  # ('seg', 'Segunda'), ('ter', 'Terça'), ...
        widget=forms.CheckboxSelectMultiple,
        label="Dias da semana para receber notificação"
    )

    class Meta:
        model = Url
        fields = ['url', 'frequencia_minutos', 'receber_notificacoes', 'dias_da_semana']

    def clean_dias_da_semana(self):
        dias = self.cleaned_data.get('dias_da_semana', [])
        return ",".join(dias)
