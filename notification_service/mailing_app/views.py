import requests
import json 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from .models import Mailing, Client, Message


from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

import logging
logger = logging.getLogger('mailing_app')

class MailingView(ModelViewSet):

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True, methods=['get'])
    def stat(self, request, pk):
        queryset = Mailing.objects.filter(id=pk).all()
        serializer = MailingSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullstat(self, request):
        content = MailingView.get_statistic()
        return Response(content)

    @staticmethod
    def get_statistic():
        mailing = Mailing.objects.all()
        count_all = Mailing.objects.all().count()
        content = {'Number of Mailings': count_all,
                   'Statistic for Mailing': ''}
        res = {}

        for row in mailing:
            message = Message.objects.filter(mailing_id=row.id).all()
            not_sent = message.filter(status='Not sent').count()
            sent = message.filter(status='Sent').count()

            message_stat = {'Sent messages': sent, 'Unsent messages': not_sent}
            res[f'id = {row.id}'] = message_stat

        content['Statistic for Mailing'] = res
        return content


class ClientView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class MessageView(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

