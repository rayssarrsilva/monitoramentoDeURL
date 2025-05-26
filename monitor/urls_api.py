from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import UrlViewSet, NotificacaoViewSet

router = DefaultRouter()
router.register(r'urls', UrlViewSet, basename='url')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')

urlpatterns = router.urls + [
    path('token/', obtain_auth_token, name='api_token_auth'),
]
