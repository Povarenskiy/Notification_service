import requests
import time
import logging
import sys

from logging import StreamHandler, Formatter


from datetime import datetime, timezone, timedelta

from django.conf import settings
from .models import Message


logger = logging.getLogger('__name__')
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def send_message(data, start, end, url=settings.URL, token=settings.TOKEN, attempt=0):
    now = datetime.now(timezone.utc)

    if now < end:
        if now > start:
            header = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'}
            try:
                requests.post(url=url + str(data['id']), headers=header, json=data)
            except requests.exceptions.RequestException as error:
                restarting_time = 2 ** attempt
                logger.info(f"Error sending the message id: {data['id']}, restarting via {restarting_time} s")
                time.sleep(restarting_time)
                attempt += 1
                raise send_message(data, start, end, attempt=attempt)
            else:
                Message.objects.filter(pk=data['id']).update(status='Sent')
                logger.info(f"The message id: {data['id']} sent'")
        else:
            sleeping_time = (start - now) / timedelta(seconds=1)
            time.sleep(sleeping_time)
            logger.info(f"Sending a message id: {data['id']} is registered, sending via {sleeping_time} s")
    else:
        logger.info(f"The time for sending the message id: {data['id']} has expired")
