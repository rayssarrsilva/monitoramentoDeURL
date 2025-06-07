from django.shortcuts import render
from .models import Url, Notificacao, StatusHistorico, HistoricoDeAcesso
from django.contrib.auth.decorators import login_required
from .forms import UrlForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.utils import timezone
from django.contrib import messages


# Create your views here.

@login_required
def lista_urls(request):
    urls = Url.objects.filter(usuario = request.user) #lista por ORM, mostrando apenas as urls do user
    return render(request, 'monitor/lista.html', {'urls': urls})


def verificar_status(url):
    try:
        response = requests.get(url, timeout=5)
        return 'online' if response.status_code == 200 else 'offline'
    except:
        return 'offline'

@login_required
def criar_url(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.usuario = request.user
            url.statusAtual = verificar_status(url.url)

            url.receber_notificacoes = form.cleaned_data.get('receber_notificacoes', False)

            dias = form.cleaned_data.get('dias_da_semana')
            url.dias_da_semana = ",".join(dias) if isinstance(dias, list) else dias

            url.save()

            HistoricoDeAcesso.objects.create(
                usuario=request.user,
                url=url,
                status=url.statusAtual,
                data=timezone.now()
            )

            return redirect('lista_urls')
    else:
        form = UrlForm()
    return render(request, 'monitor/form.html', {'form': form})

@login_required
def desativar_notificacoes(request, url_id):
    url = get_object_or_404(Url, id=url_id, usuario=request.user)
    url.receber_notificacoes = False
    url.frequencia_minutos = None
    url.dias_da_semana = ""
    url.save()
    messages.success(request, "Notificações desativadas com sucesso.")
    return redirect('notificacoes')

@login_required
def reativar_notificacoes(request, url_id):
    url = get_object_or_404(Url, id=url_id, usuario=request.user)
    url.receber_notificacoes = True
    url.save()
    messages.success(request, "Notificações reativadas com sucesso.")
    return redirect('notificacoes')

@login_required
def excluir_url(request, id):
    url = get_object_or_404(Url, id=id, usuario=request.user)
    url.delete()
    return redirect('lista_urls')

@login_required
def lista_notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-enviado_em')
    return render(request, 'monitor/notificacoes.html', {'notificacoes': notificacoes})

@login_required
def historico_acessos(request):
    acessos = HistoricoDeAcesso.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'monitor/acessos.html', {'acessos': acessos})

@login_required
def dashboard(request):
    total = Url.objects.filter(usuario=request.user).count()
    offline = Url.objects.filter(usuario=request.user,statusAtual='offline').count()
    online = Url.objects.filter(usuario=request.user,statusAtual='online').count()
    return render(request, 'monitor/dashboard.html', {'total': total, 'offline': offline, 'online': online})

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Autenticar manualmente após criar
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  

    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registrar.html', {'form': form})

def homepage(request):
    return render(request, 'monitor/home.html')

def fazer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def fazer_logout(request):
    logout(request)
    return redirect('login')

