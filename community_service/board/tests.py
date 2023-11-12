import uuid
from rest_framework.test import APITestCase

from .models import Forum, Post

class ForumTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/forums/"

    def test_forum(self):
        Forum.objects.create(forum_name="test_forum1")
        Forum.objects.create(forum_name="test_forum2")
        Forum.objects.create(forum_name="test_forum3", allow_anonymous=True)
        Forum.objects.create(forum_name="test_forum4", allow_anonymous=True)

        response = self.client.post(self.url, data={"forum_name": "test_forum5"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["forum_name"], "test_forum5")
        self.assertEqual(response.data["allow_anonymous"], False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

        response = self.client.delete(self.url + "5/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Forum.objects.get(id=5).is_deleted, True)
        self.assertEqual(len(Forum.objects.all()), 5)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_forum_failure(self):
        Forum.objects.create(forum_name="test_forum1")
        response = self.client.post(self.url, data={"forum_name": "test_forum1"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 405)

class PostTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/posts/"
        self.user_uuid = uuid.uuid4()
        self.forum1 = Forum.objects.create(forum_name="test_forum1")
        self.forum2 = Forum.objects.create(forum_name="test_forum2")

    def test_post(self):
        post1 = Post.objects.create(
            forum=self.forum1,
            author_uuid=self.user_uuid,
            title="test_title1",
            content="test_content1"
        )
        Post.objects.create(
            forum=self.forum1,
            author_uuid=self.user_uuid,
            title="test_title2",
            content="test_content2"
        )
        Post.objects.create(
            forum=self.forum2,
            author_uuid=self.user_uuid,
            title="test_title3",
            content="test_content3"
        )
        Post.objects.create(
            forum=self.forum1,
            author_uuid=self.user_uuid,
            title="test_title4",
            content="test_content4",
            is_deleted=True
        )

        response = self.client.get(self.url + f"?forum_id={self.forum1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.delete(self.url + f"{post1.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.get(id=post1.id).is_deleted, True)
        self.assertEqual(len(Post.objects.all()), 4)

    def test_post_fail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
