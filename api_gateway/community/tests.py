from unittest.mock import patch
import requests_mock
from rest_framework.test import APITestCase

class TagAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    def test_tag_list(self, m):
        m.get(
            self.community_server + '/api/tags/',
            json=[{'id': 1, 'name': '태그1'}],
            status_code=200
        )
        self.client.get('/api/community/tags/')

class ImageAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_image_create(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/images/', {'image': 'image'})

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/images/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/images/', {'image': 'image'})

class PostAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_post_create(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/posts/', {'content': 'content'})

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/posts/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/posts/', {'content': 'content'})

    @requests_mock.Mocker()
    def test_post_list(self, m):
        m.get(
            self.community_server + '/api/posts/',
            json=[{'id': 1, 'content': 'content'}],
            status_code=200
        )
        self.client.get('/api/community/posts/')

class PostDetailAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    def test_post_detail(self, m):
        m.get(
            self.community_server + '/api/posts/1/',
            json={'id': 1, 'content': 'content'},
            status_code=200
        )
        self.client.get('/api/community/posts/1/')
