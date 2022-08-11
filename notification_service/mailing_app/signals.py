import threading

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Mailing, Client, Message
from .thread import send_message


@receiver(post_save, sender=Mailing)
def create_message(sender, instance, created, **kwargs):

    if created:
        clients = Client.objects.filter(tag=instance.tag).\
            filter(phone_number__istartswith='7'+instance.mobile_operator_code).all()

        for client in clients:
            Message.objects.create(
                status='Unsent',
                client_id=client.id,
                mailing_id=instance.id
            )
            new_message = Message.objects.filter(mailing_id=instance.id).first()
            time_start = instance.time_start
            time_end = instance.time_end
            send_data = {
                'id': new_message.id,
                'phone number': client.phone_number,
                'text': instance.text
            }

            threading.Thread(target=send_message, args=(send_data, time_start, time_end, )).start()
