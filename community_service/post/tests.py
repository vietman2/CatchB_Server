from unittest.mock import patch
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from comment.models import Comment
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
        self.user_uuid = '123e4567-e89b-12d3-a456-426614174000'
        self.post_pk = '2024031500000001'
        ## setup comment data to raise coverage (cover all times)
        ## 1. created less than 1 minute ago
        Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment now',
        )
        ## 2. created less than 1 hour ago
        minutes = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment minutes',
        )
        minutes.created_at = timezone.now() - timezone.timedelta(minutes=30)
        minutes.save()
        ## 3. created less than 1 day ago
        hours = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment hours',
        )
        hours.created_at = timezone.now() - timezone.timedelta(hours=12)
        hours.save()
        ## 4. created less than 1 week ago
        days = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment days',
        )
        days.created_at = timezone.now() - timezone.timedelta(days=3)
        days.save()
        ## 5. created less than 1 month ago
        weeks = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment weeks',
        )
        weeks.created_at = timezone.now() - timezone.timedelta(weeks=2)
        weeks.save()
        ## 6. created less than 1 year ago
        months = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment months',
        )
        months.created_at = timezone.now() - timezone.timedelta(weeks=30)
        months.save()
        ## 7. created more than 1 year ago
        years = Comment.objects.create(
            post_id=self.post_pk,
            commenter_uuid=self.user_uuid,
            content='comment years',
        )
        years.created_at = timezone.now() - timezone.timedelta(weeks=60)
        years.save()

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
        Comment.objects.all().delete()
        Post.objects.all().delete()
        self.data['forum'] = '덕아웃'
        self.client.post(self.url, self.data, format='json')

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
        # 1. user not logged in
        response = self.client.get(self.url + self.post_pk + '/')
        self.assertEqual(response.status_code, 200)

        # 2. user logged in
        response = self.client.get(self.url + self.post_pk + '/', {'uuid': self.user_uuid})
        self.assertEqual(response.status_code, 200)
        print(response.data)

        # 3. update viewed_last_at
        response = self.client.get(self.url + self.post_pk + '/', {'uuid': self.user_uuid})
        self.assertEqual(response.status_code, 200)

    def test_like_dislike(self):
        # 1. like
        response = self.client.post(
            self.url + '2024031500000001/like/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

        # 2. un-like
        response = self.client.post(
            self.url + '2024031500000001/like/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

        # 3. dislike
        response = self.client.post(
            self.url + '2024031500000001/dislike/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

        # 4. un-dislike
        response = self.client.post(
            self.url + '2024031500000001/dislike/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

        # 5. like then dislike
        self.client.post(
            self.url + '2024031500000001/like/',
            {'user_uuid': self.user_uuid}
        )
        response = self.client.post(
            self.url + '2024031500000001/dislike/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

        # 6. dislike then like
        response = self.client.post(
            self.url + '2024031500000001/like/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 200)

    def test_like_dislike_fail(self):
        # 1. no user_uuid
        response = self.client.post(
            self.url + '2024031500000001/like/',
            {'user_uuid': ''}
        )
        self.assertEqual(response.status_code, 400)

        # 2. no user_uuid
        response = self.client.post(
            self.url + '2024031500000001/dislike/',
            {'user_uuid': ''}
        )
        self.assertEqual(response.status_code, 400)

        # 3. no post
        response = self.client.post(
            self.url + '2022031500000002/like/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 404)

        # 4. no post
        response = self.client.post(
            self.url + '2022031500000002/dislike/',
            {'user_uuid': self.user_uuid}
        )
        self.assertEqual(response.status_code, 404)
