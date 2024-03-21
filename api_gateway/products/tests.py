from unittest.mock import patch
import requests_mock
from rest_framework.test import APITestCase

class RegionsAPITests(APITestCase):
    def setUp(self):
        self.api_server = 'http://localhost:8004/api/regions/'

    @requests_mock.Mocker()
    def test_region_get(self, m):
        m.get(
            self.api_server,
            json={'name': 'testregion'},
            status_code=200
        )
        self.client.get('/api/products/regions/')

class FacilityAPITests(APITestCase):
    def setUp(self):
        self.api_server = 'http://localhost:8004/api/facilities/'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_facility_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/facilities/')

        # 2: Success
        m.post(
            self.api_server,
            json={'name': 'testfacility'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/facilities/', data={})

    @requests_mock.Mocker()
    def test_facility_get(self, m):
        m.get(
            self.api_server,
            json={'name': 'testfacility'},
            status_code=200
        )
        self.client.get('/api/products/facilities/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_facility_info_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/facilities/123/')

        # 2: Success
        m.post(
            self.api_server + '123/info/',
            json={'name': 'testfacility'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/facilities/123/', data={})

    @requests_mock.Mocker()
    def test_facility_info_get(self, m):
        m.get(
            self.api_server + '123/',
            json={'name': 'testfacility'},
            status_code=200
        )
        self.client.get('/api/products/facilities/123/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_facility_status_get(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.get('/api/products/facilities/status/')

        # 2: Success
        m.get(
            self.api_server + 'status/',
            json={'name': 'testfacility'},
            status_code=200
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.get('/api/products/facilities/status/')

class CoachAPITests(APITestCase):
    def setUp(self):
        self.api_server = 'http://localhost:8004/api/coaches/'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_coach_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/coaches/')

        # 2: Success
        m.post(
            self.api_server,
            json={'name': 'testcoach'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/coaches/', data={})

    @requests_mock.Mocker()
    def test_coach_get(self, m):
        m.get(
            self.api_server,
            json={'name': 'testcoach'},
            status_code=200
        )
        self.client.get('/api/products/coaches/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_coach_info_post(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/products/coaches/123/')

        # 2: Success
        m.post(
            self.api_server + '123/info/',
            json={'name': 'testcoach'},
            status_code=201
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.post('/api/products/coaches/123/', data={})

    @requests_mock.Mocker()
    def test_coach_info_get(self, m):
        m.get(
            self.api_server + '123/',
            json={'name': 'testcoach'},
            status_code=200
        )
        self.client.get('/api/products/coaches/123/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_coach_status_get(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.get('/api/products/coaches/status/')

        # 2: Success
        m.get(
            self.api_server + 'status/',
            json={'name': 'testcoach'},
            status_code=200
        )
        mock_get_user_info.return_value = {'user_id': '1'}
        self.client.get('/api/products/coaches/status/')
