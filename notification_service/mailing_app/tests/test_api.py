from rest_framework.test import APITestCase, RequestsClient
from django.utils.timezone import now, timedelta
from rest_framework import status


class TestApi(APITestCase):


    @classmethod
    def setUpTestData(self):
        self.test_code = '999'
        self.test_tag = '1'

        self.url = 'http://127.0.0.1:8000/api'
        
        new_client = {
            'tag': self.test_tag,
            'phone_number': f'7{self.test_code}1111111',
        }

        new_mailing = {
            'time_start': now(),
            'time_end': now() + timedelta(minutes=30),
            'text': 'Some text',
            'client_tag': self.test_tag,
            'client_mobile_operator_code': self.test_code,
        }

        self.client = RequestsClient()

        self.client_responce = self.client.post(f'{self.url}/client/', new_client)
        self.mailing_responce = self.client.post(f'{self.url}/mailing/', new_mailing)


    def test_client_api(self):
        self.assertEqual(self.client_responce.status_code, status.HTTP_201_CREATED)
       

    def test_mailing_api(self):
        self.assertEqual(self.mailing_responce.status_code, status.HTTP_201_CREATED)


    def test_message(self):
        message_responce = self.client.get(f'{self.url}/message/1/')
        self.assertEqual(message_responce.status_code, status.HTTP_200_OK)
        self.assertEqual(message_responce.data['client'], 1)
        self.assertEqual(message_responce.data['mailing'], 1)
        

    def test_info(self):
        stat_responce = self.client.get(f'{self.url}/mailing/1/stat/')
        self.assertEqual(stat_responce.status_code, status.HTTP_200_OK)
        
        fullstat_responce = self.client.get(f'{self.url}/mailing/fullstat/')
        self.assertEqual(fullstat_responce.status_code, status.HTTP_200_OK)
        self.assertEqual(fullstat_responce.data['Number of Mailings'], 1)
        self.assertIsInstance(fullstat_responce.data['Statistic for Mailing'], dict)

