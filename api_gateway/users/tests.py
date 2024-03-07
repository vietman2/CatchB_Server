from unittest.mock import patch
import requests_mock
from rest_framework.test import APITestCase

class UsersAPITests(APITestCase):
    def setUp(self):
        self.user_server = 'http://localhost:8005'

    @requests_mock.Mocker()
    def test_signup(self, m):
        m.post(
            self.user_server + '/api/users/register/',
            json={'username': 'testuser', 'password': 'testpassword'},
            status_code=201
        )
        self.client.post('/api/users/register/', {
            'username': 'testuser',
            'password': 'testpassword',
        })

    @requests_mock.Mocker()
    def test_login(self, m):
        m.post(
            self.user_server + '/api/login/',
            json={'token': 'testtoken'},
            status_code=200
        )
        self.client.post('/api/users/login/', {
            'username': 'testuser',
            'password': 'testpassword',
        })

    @requests_mock.Mocker()
    def test_logout(self, m):
        m.post(
            self.user_server + '/api/logout/',
            status_code=204
        )
        self.client.post('/api/users/logout/')

    @requests_mock.Mocker()
    def test_password_change(self, m):
        m.post(
            self.user_server + '/api/users/password_change/',
            status_code=200
        )
        self.client.post('/api/users/password_change/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_userinfo_get(self, m, mock_get_user_info):
        m.get(
            self.user_server + '/api/users/1/',
            json={'user_id': '1'},
            status_code=200
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.get('/api/users/1/')

        self.client.get('/api/users/2/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_userinfo_delete(self, m, mock_get_user_info):
        m.delete(
            self.user_server + '/api/users/1/',
            status_code=204
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.delete('/api/users/1/')

        self.client.delete('/api/users/2/')

    @requests_mock.Mocker()
    def test_token_refresh(self, m):
        m.post(
            self.user_server + '/api/token/refresh/',
            json={'token': 'testtoken'},
            status_code=200
        )
        self.client.post('/api/users/token/refresh/')

    @requests_mock.Mocker()
    def test_coupons_register(self, m):
        m.post(
            self.user_server + '/api/coupons/register/',
            status_code=201
        )
        self.client.post('/api/users/coupons/register/')

    @requests_mock.Mocker()
    def test_coupons_status(self, m):
        m.get(
            self.user_server + '/api/coupons/status/',
            json={'status': 'teststatus'},
            status_code=200
        )
        self.client.get('/api/users/coupons/status/')

    @requests_mock.Mocker()
    def test_coupons_list(self, m):
        m.get(
            self.user_server + '/api/coupons/',
            json={'coupons': 'testcoupons'},
            status_code=200
        )
        self.client.get('/api/users/coupons/')

    @requests_mock.Mocker()
    def test_points(self, m):
        m.get(
            self.user_server + '/api/points/',
            json={'points': 'testpoints'},
            status_code=200
        )
        self.client.get('/api/users/points/')
