import requests_mock
from rest_framework.test import APITestCase

class BankAPITests(APITestCase):
    def setUp(self):
        self.payments_server = 'http://localhost:8003'

    @requests_mock.Mocker()
    def test_bank_list(self, m):
        m.get(
            self.payments_server + '/api/banks/',
            json=[{'id': 1, 'name': '국민은행'}],
            status_code=200
        )
        self.client.get('/api/payments/banks/')
        ## TODO: mock tokens

    @requests_mock.Mocker()
    def test_bank_list_unauthorized(self, m):
        m.get(
            self.payments_server + '/api/banks/',
            status_code=401
        )
        self.client.get('/api/payments/banks/')
