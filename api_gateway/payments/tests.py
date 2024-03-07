from unittest.mock import patch
import requests_mock
from rest_framework.test import APITestCase

class BankAPITests(APITestCase):
    def setUp(self):
        self.payments_server = 'http://localhost:8003'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_bank_list(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.get('/api/payments/banks/')

        # 2: Success
        m.get(
            self.payments_server + '/api/banks/',
            json=[{'id': 1, 'name': '국민은행'}],
            status_code=200
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.get('/api/payments/banks/')
