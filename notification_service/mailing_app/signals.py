import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Mailing, Client, Message
from .tasks import send_message


logger = logging.getLogger('mailing_app')

@receiver(post_save, sender=Mailing)
def create_message(sender, instance, created, **kwargs):
    """
    Отправка сообщения по списку клиентам по тэгу и номеру телефона 
    с сохранением в базу данных
    """
    clients = Client.objects.filter(
        tag=instance.client_tag,
        mobile_operator_code=instance.client_mobile_operator_code).all()

    for client in clients:
        new_message = Message.objects.create(
            client_id=client.id,
            mailing_id=instance.id
        )
        send_data = {
            'id': new_message.id,
            'client': new_message.client.id,
            'phone number': new_message.client.phone_number,
            'text': instance.text
        }
        time_start = instance.time_start
        time_end = instance.time_end
        send_message.apply_async(args=[send_data], eta=time_start, expires=time_end)
   


