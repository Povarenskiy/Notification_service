import requests
import time
import logging

from datetime import datetime, timezone, timedelta

from django.conf import settings
from .models import Message


logger = logging.getLogger('mailing_app')


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
                logger.info(f"The message id: {data['id']} sent to phone number: {data['phone number']}")
        else:
            sleeping_time = (start - now) / timedelta(seconds=1)
            logger.info(f"Sending a message id: {data['id']} is registered, sending via {sleeping_time} s")
            time.sleep(sleeping_time)
            return send_message(data, start, end)
    else:
        logger.info(f"The time for sending the message id: {data['id']} has expired")
