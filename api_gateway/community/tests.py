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

    @requests_mock.Mocker()
    def test_post_detail_logged_in(self, m):
        with patch("community.views.get_user_info") as mock_get_user_info, \
             patch("core.permissions.IsLoggedIn.has_permission") as mock_has_permission:
            mock_get_user_info.return_value = {'user_id': '1'}
            mock_has_permission.return_value = True
            m.get(
                self.community_server + '/api/posts/1/',
                json={'id': 1, 'content': 'content'},
                status_code=200
            )
            self.client.get('/api/community/posts/1/')

class PostLikeDislikeAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_post_like(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/posts/1/like/')

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/posts/1/like/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/posts/1/like/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_post_dislike(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/posts/1/dislike/')

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/posts/1/dislike/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/posts/1/dislike/')

class CommentAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_comment_create(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/comments/', {'content': 'content'})

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/comments/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/comments/', {'content': 'content'})

    @requests_mock.Mocker()
    def test_comment_list(self, m):
        m.get(
            self.community_server + '/api/comments/',
            json=[{'id': 1, 'content': 'content'}],
            status_code=200
        )
        self.client.get('/api/community/comments/')

    @requests_mock.Mocker()
    def test_comment_list_logged_in(self, m):
        with patch("community.views.get_user_info") as mock_get_user_info, \
             patch("core.permissions.IsLoggedIn.has_permission") as mock_has_permission:
            mock_get_user_info.return_value = {'user_id': '1'}
            mock_has_permission.return_value = True
            m.get(
                self.community_server + '/api/comments/',
                json=[{'id': 1, 'content': 'content'}],
                status_code=200
            )
            self.client.get('/api/community/comments/')

class CommentLikeDislikeAPITests(APITestCase):
    def setUp(self):
        self.community_server = 'http://localhost:8002'

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_comment_like(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/comments/1/like/')

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/comments/1/like/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/comments/1/like/')

    @requests_mock.Mocker()
    @patch("core.permissions.get_user_info")
    def test_comment_dislike(self, m, mock_get_user_info):
        # 1: Fail: 401 Unauthorized
        mock_get_user_info.return_value = None
        self.client.post('/api/community/comments/1/dislike/')

        # 2: Success
        mock_get_user_info.return_value = {'user_id': '1'}
        m.post(
            self.community_server + '/api/comments/1/dislike/',
            json={'id': 1},
            status_code=201
        )
        self.client.post('/api/community/comments/1/dislike/')
