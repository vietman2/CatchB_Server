from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from .models import Tag

class TagAPITest(APITestCase):
    def setUp(self):
        self.url = '/api/tags/'

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class ImageUploadAPITest(APITestCase):
    def setUp(self):
        self.url = '/api/images/'
        self.file = SimpleUploadedFile('test.png', b'file_content', content_type='image/png')
        self.data = {
            'image': self.file,
            'user_uuid': '123e4567-e89b-12d3-a456-426614174000'
        }

    @patch('django.core.files.storage.FileSystemStorage._save')
    def test_create(self, mock_save):
        response = self.client.post(self.url, self.data, format='multipart')
        self.assertEqual(response.status_code, 201)

class PostAPITest(APITestCase):
    def setUp(self):
        self.url = '/api/posts/'
        self.data = {
            'title': 'test title',
            'content': 'test content',
            'author_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'tags': [1, 2],
            'images': []
        }
        Tag.objects.create(name='test1', icon='test1', color='test1', bgcolor='test1', forum=1)
        Tag.objects.create(name='test2', icon='test2', color='test2', bgcolor='test2', forum=1)
        Tag.objects.create(name='test3', icon='test3', color='test3', bgcolor='test3', forum=1)
        Tag.objects.create(name='test4', icon='test4', color='test4', bgcolor='test4', forum=1)

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

    def test_create_fail(self):
        self.data['forum'] = '덕아웃'
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        self.data['title'] = ""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        self.data['title'] = "new title"
        self.data['tags'] = [1, 2, 3, 4]
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        self.data['forum'] = '테스트'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)
