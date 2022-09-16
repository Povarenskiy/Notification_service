from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from .models import Mailing, Client, Message


class MailingView(ModelViewSet):

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True, methods=['get'])
    def callinfo(self, request, pk):
        queryset = Mailing.objects.filter(id=pk).all()
        serializer = MailingSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def callfullinfo(self, request):
        mailing = Mailing.objects.all()
        count_all = Mailing.objects.all().count()
        content = {'Number of Mailings': count_all,
                   'Statistic for Mailing': ''}
        res = {}

        for row in mailing:
            message = Message.objects.filter(mailing_id=row.id).all()
            not_sent = message.filter(status='Not sent').count()
            sent = message.filter(status='Sent').count()

            message_stat = {'Number of sent messages': sent, 'Number of Not sent messages': not_sent}
            res[f'id = {row.id}'] = message_stat

        content['Statistic for Mailing'] = res
        return Response(content)


class ClientView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageView(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

