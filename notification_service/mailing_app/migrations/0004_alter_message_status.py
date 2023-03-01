# Generated by Django 4.1.7 on 2023-03-01 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0003_remove_message_is_sent_message_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[(False, 'Not sent'), (True, 'Sent')], default=False, max_length=5, verbose_name='Статус отправки'),
        ),
    ]
