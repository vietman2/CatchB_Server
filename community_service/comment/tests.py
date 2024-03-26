from rest_framework.test import APITestCase

class CommentAPITestCase(APITestCase):
    fixtures = ['init_data.json', 'test_data.json']

    def setUp(self):
        self.url = '/api/comments/'
        self.commenter_uuid = '123e4567-e89b-12d3-a456-426614174000'
        self.post_pk = 2024031500000001

    def test_create_success(self):
        data = {
            'post': self.post_pk,
            'commenter_uuid': self.commenter_uuid,
            'content': 'test content'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_fail(self):
        # 1. no post
        data = {
            'commenter_uuid': self.commenter_uuid,
            'content': 'test content'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

        # 2. no commenter_uuid
        data = {
            'post': self.post_pk,
            'content': 'test content'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

        # 3. no content
        data = {
            'post': self.post_pk,
            'commenter_uuid': self.commenter_uuid
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
