from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch, Count, Q


from .serializers import *
from .models import *
from .services import get_mailing_statistics


class MailingView(ModelViewSet):
    """Отображение рассылок"""
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True)
    def stat(self, request, pk):
        """Статистика по конкретной рассылке"""
        content = get_mailing_statistics(pk)
        return Response(content)

    @action(detail=False)
    def fullstat(self, request):
        """Статистика по рассылкам"""
        content = get_mailing_statistics()
        return Response(content)


class ClientView(ModelViewSet):
    """Отображение клиентов"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class MessageView(ModelViewSet):
    """Отображение сообщений"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

