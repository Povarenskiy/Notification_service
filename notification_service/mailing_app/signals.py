from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Mailing, Client, Message
from .tasks import send_message

import logging


logger = logging.getLogger('mailing_app')

@receiver(post_save, sender=Mailing)
@receiver(post_save, sender=Client)
@receiver(post_save, sender=Message)
def logging_save_and_create_message(sender, instance, created, **kwargs):
    if created:
        logger.info(f'{instance} created')
        
        if sender == Mailing:
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
    else:
        logger.info(f'{instance} updated')


@receiver(post_delete, sender=Mailing)
@receiver(post_delete, sender=Client)
@receiver(post_delete, sender=Message)
def logging_delete(sender, instance, **kwargs):
    logger.info(f'{instance} deleted')
    

