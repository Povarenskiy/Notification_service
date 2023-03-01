import requests
import logging

from notification_service.celery import app
from celery.exceptions import MaxRetriesExceededError
from celery import shared_task
from requests.exceptions import HTTPError
from django.conf import settings
from django.db.models import Prefetch
from django.core.mail import send_mail

from .models import Message, Mailing
from .services import get_mailing_statistics


logger = logging.getLogger('mailing_app')

@app.task(bind=True, retry_backoff=True, max_retries=5)
def send_message(self, data, url=settings.URL, token=settings.TOKEN):
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
        Message.objects.filter(pk=data['id']).update(status=True)
        logger.info(f"Message id: {data['id']} sent to Client id: {data['client']} with phone number: {data['phone number']}")


@shared_task
def statistics_report(emails=settings.EMAIL):
    message = str(get_mailing_statistics())
    subject = 'Statistics report for Mailing'            
    host = settings.EMAIL_HOST_USER

    if emails:
        send_mail(subject, message, host, emails, fail_silently=False)
        logger.info(f'Statistic report send to {emails}')
    else:
        logger.info(f'Email is not set')
