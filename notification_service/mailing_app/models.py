import pytz
from django.core.validators import RegexValidator
from django.db import models


class Mailing(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    text = models.TextField(max_length=255)
    tag = models.CharField(max_length=10)
    mobile_operator_code = models.CharField(max_length=3)


class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="The phone number in the format: 7XXXXXXXXXX, where X - number from 0 to 9")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True)

    tag = models.CharField(max_length=10)

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Message(models.Model):
    time_mailing = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

