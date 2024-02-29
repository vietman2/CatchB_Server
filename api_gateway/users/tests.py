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
    def test_user_self_get(self, m):
        m.get(
            self.user_server + '/api/users/1/',
            status_code=200,
            headers={'Content-Type': 'application/json'},
        )
        self.client.get('/api/users/', {'uuid': '1'})
        ## TODO: mock tokens
