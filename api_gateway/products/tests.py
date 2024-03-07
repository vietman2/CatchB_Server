from unittest.mock import patch
import requests_mock
from rest_framework.test import APITestCase

class ProductsAPITests(APITestCase):
    def setUp(self):
        self.products_server = 'http://localhost:8004'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_facility_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/facilities/')

        # 2: Success
        m.post(
            self.products_server + '/api/facilities/',
            json={'name': 'testfacility'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/facilities/', data={})

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_facility_info_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/facilities/123/')

        # 2: Success
        m.post(
            self.products_server + '/api/facilities/123/info/',
            json={'name': 'testfacility'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/facilities/123/', data={})

    @requests_mock.Mocker()
    def test_region_get(self, m):
        m.get(
            self.products_server + '/api/regions/',
            json={'name': 'testregion'},
            status_code=200
        )
        self.client.get('/api/products/regions/')
