from notification_service.celery import app
from celery.exceptions import MaxRetriesExceededError
from django.conf import settings
from .models import Mailing, Message
from dotenv import load_dotenv

import os
import requests
import logging

load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')

logger = logging.getLogger('mailing_app')


@app.task(bind=True, retry_backoff=True, max_retries=5)
def send_message(self, data, url=URL, token=TOKEN):
    try:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.info(f"Error sending the message id: {data['id']}")
            raise self.retry(exc=exc)
        else:
            Message.objects.filter(pk=data['id']).update(status='Sent')
            logger.info(f"The message id: {data['id']} sent to phone number: {data['phone number']}")
    except MaxRetriesExceededError:
        logger.info(f"Max retries exceeded for sending the message id: {data['id']}")

