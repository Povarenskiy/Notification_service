from rest_framework.test import APITestCase
from mailing_app.models import Client, Mailing, Message
from django.utils.timezone import now, timedelta


class TestModels(APITestCase):

    @classmethod
    def setUpTestData(self):
        test_code = '999'
        test_tag = '1'

        client = Client.objects.create(
            tag = test_tag,
            phone_number = f'7{test_code}1111111'
        )

        mailing = Mailing.objects.create(
            time_start = now(),
            time_end = now() + timedelta(minutes=30),
            text = 'Some text',
            client_tag = test_tag,
            client_mobile_operator_code = test_code,
        )

        Message.objects.create(
            status = 'NOT',
            time_creation = now(),
            client = client,
            mailing = mailing,
        )


    def test_client(self):
        client = Client.objects.get(id=1)
        self.assertIsInstance(client, Client)
        self.assertIsInstance(client.phone_number, str)
        self.assertEqual(client.mobile_operator_code, '999')

    
    def test_mailing(self):
        mailing = Mailing.objects.get(id=1)
        self.assertIsInstance(mailing, Mailing)
        self.assertIsInstance(mailing.text, str)
        self.assertEqual(mailing.client_mobile_operator_code, '999')
        self.assertEqual(mailing.client_tag, '1')


    def test_message(self):
        message = Message.objects.get(id=1)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.client_id, 1)
        self.assertEqual(message.mailing_id, 1)
    
            