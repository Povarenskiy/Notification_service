import pytz
from django.core.validators import RegexValidator
from django.db import models


class Mailing(models.Model):
    time_start = models.DateTimeField(verbose_name='Время начала отправки')
    time_end = models.DateTimeField(verbose_name='Время конца отправки')
    text = models.TextField(max_length=255, verbose_name='Текст сообщения')
    client_tag = models.CharField(max_length=10, verbose_name='Тег для фильтрации клиентов')
    client_mobile_operator_code = models.CharField(max_length=3, verbose_name='Мобильный оператор для фильтрации клиентов')

    def __str__(self):
        return f'Mailing id: {self.id}'
        

class Client(models.Model):
    tag = models.CharField(max_length=10, verbose_name='Тег клиента')
    phone_regex = RegexValidator(regex=r'^7\d{10}$', message="Номер телефона в формате: 7XXXXXXXXXX, где Х - число от 0 до 9")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name='Номер телефона')
    mobile_operator_code = models.CharField(max_length=3, editable=False, verbose_name='Мобильный оператор клиента')
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC', verbose_name='Часовой пояс')

    def __str__(self):
        return f'Client id: {self.id}'

    def save(self, *args, **kwargs):
        print(args, kwargs)
        self.mobile_operator_code = self.phone_number[1:4]
        return super(Client, self).save(*args, **kwargs)


class Message(models.Model):
    SENDING_STATUS_CHOICES = (
        ('NOT', 'Not sent'),
        ('YES', 'Sent')
    )
    status = models.CharField(max_length=3, choices=SENDING_STATUS_CHOICES, default='NOT', verbose_name='Статус отправки')
    time_creation = models.DateTimeField(auto_now_add=True, verbose_name='Время создания сообщения')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f'Message id: {self.id}'
