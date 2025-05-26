from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.fazer_login, name='login'),
    path('logout/', views.fazer_logout, name='logout'),
    path('urls/', views.lista_urls, name='lista_urls'),
    path('urls/criar/', views.criar_url, name='criar_url'),
    path('urls/<int:id>/excluir/', views.excluir_url, name='excluir_url'),
    path('notificacoes/', views.lista_notificacoes, name='notificacoes'),
    path('notificacoes/desativar/<int:url_id>/', views.desativar_notificacoes, name='desativar_notificacoes'),
    path('notificacoes/reativar/<int:url_id>/', views.reativar_notificacoes, name='reativar_notificacoes'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('acessos/', views.historico_acessos, name='historico_acessos'),
    path('registrar/', views.registrar, name='registrar'),
]