from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from .models import Post

class TagAPITest(APITestCase):
    fixtures = ['init_data.json']

    def test_list(self):
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/api/tags/1/')
        self.assertEqual(response.status_code, 405)

class ImageUploadAPITest(APITestCase):
    def setUp(self):
        self.url = '/api/images/'
        self.file = SimpleUploadedFile('test.png', b'file_content', content_type='image/png')
        self.data = {
            'image': self.file,
            'user_uuid': '123e4567-e89b-12d3-a456-426614174000'
        }

    @patch('django.core.files.storage.default_storage.save')
    def test_create(self, mock_save):
        mock_save.return_value = 'test.png'
        response = self.client.post(self.url, self.data, format='multipart')
        self.assertEqual(response.status_code, 201)

class PostAPITest(APITestCase):
    fixtures = ['init_data.json', 'test_data.json']

    def setUp(self):
        self.url = '/api/posts/'
        self.data = {
            'title': 'test title',
            'content': 'test content',
            'author_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'tags': [1, 2],
            'images': []
        }

    def test_create_success(self):
        self.data['forum'] = '덕아웃'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)

        self.data['forum'] = '드래프트'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)

        self.data['forum'] = '장터'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)

        self.data['forum'] = '스틸'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_primary_key(self):
        ## delete all posts
        Post.objects.all().delete()
        self.data['forum'] = '덕아웃'
        response = self.client.post(self.url, self.data, format='json')        

    def test_create_fail(self):
        # 1. duplicate title in same forum
        self.data['forum'] = '덕아웃'
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        # 2. no title
        self.data['title'] = ""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        # 3. too many tags
        self.data['title'] = "new title"
        self.data['tags'] = [1, 2, 3, 4]
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        # 4. forum dne
        self.data['forum'] = '테스트'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_list(self):
        self.data['forum'] = '덕아웃'
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url, {'forum': '덕아웃'})
        self.assertEqual(response.status_code, 200)

    def test_list_fail(self):
        # 1. no forum (query)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_retrieve(self):
        response = self.client.get(self.url + '2024031500000001/')
        self.assertEqual(response.status_code, 200)
