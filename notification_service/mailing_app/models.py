import pytz
from django.core.validators import RegexValidator
from django.db import models


class Mailing(models.Model):
    time_start = models.DateTimeField(verbose_name='Start time of sending')
    time_end = models.DateTimeField(verbose_name='End time of sending')
    text = models.TextField(max_length=255, verbose_name='Message text')
    tag = models.CharField(max_length=10, verbose_name='Search clients by tag')
    mobile_operator_code = models.CharField(max_length=3, verbose_name='Client mobile operator code')


class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="The phone number in the format: 7XXXXXXXXXX, where X - number from 0 to 9")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name='Phone number')

    tag = models.CharField(max_length=10, verbose_name='Search tag')

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC', verbose_name='Timezone')


class Message(models.Model):
    time_mailing = models.DateTimeField(auto_now_add=True, verbose_name='Time of message creation')
    status = models.CharField(max_length=20, verbose_name='Status send or not sent')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

