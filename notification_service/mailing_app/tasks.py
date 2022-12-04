import os
import requests
import logging
import re

from notification_service.celery import app
from celery.exceptions import MaxRetriesExceededError
from celery import shared_task
from dotenv import load_dotenv
from requests.exceptions import HTTPError
from django.core.mail import send_mail
from django.conf import settings

from .models import Message
from .views import MailingView


load_dotenv()
URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')
EMAIL = os.getenv('EMAIL')
logger = logging.getLogger('mailing_app')


@app.task(bind=True, retry_backoff=True, max_retries=5)
def send_message(self, data, url=URL, token=TOKEN):
    try:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}

        response = requests.post(url=url + str(data['id']), headers=header, json=data)
        response.raise_for_status()
   
    except HTTPError as http_err:
        logger.info(f"Message id: {data['id']} HTTP error occurred {http_err} ")
        self.retry(exc=http_err)

    except MaxRetriesExceededError:
        logger.info(f"Message id: {data['id']} max retries for sending exceeded")

    except Exception as err:
        logger.info(f"Message id: {data['id']} other error occurred: {err}")
    
    else:
        Message.objects.filter(pk=data['id']).update(status='YES')
        logger.info(f"Message id: {data['id']} sent to Client id: {data['client']} with phone number: {data['phone number']}")


@shared_task
def statistics_report(email=EMAIL):
    message = str(MailingView.get_statistic())
    subject = 'Statistics report for Mailing'            
    host = 'settings.EMAIL_HOST_USER'

    regex = '([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
    email_list = re.findall(regex, email)

    if email_list:
        send_mail(subject, message, host, email_list, fail_silently=False)
        logger.info(f'Statistic report send to {email_list}')
    else:
        logger.info(f'Email is not set in .env')
