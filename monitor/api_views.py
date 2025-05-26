from rest_framework import viewsets
from .models import Url, Notificacao
from .serializers import UrlSerializer, NotificacaoSerializer
from rest_framework.permissions import IsAuthenticated

class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Url.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class NotificacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)