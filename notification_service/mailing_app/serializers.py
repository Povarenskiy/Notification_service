from rest_framework.serializers import ModelSerializer
from .models import Mailing, Client, Message


class MailingSerializer(ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
