import uuid
from rest_framework.test import APITestCase

from .models import Forum, Post, Comment, ReComment, ReportReason

class ForumTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/forums/"

    def test_init_forums(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

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
        self.assertEqual(len(response.data), 10)

        response = self.client.delete(self.url + "5/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Forum.objects.get(id=5).is_deleted, True)
        self.assertEqual(len(Forum.objects.all()), 10)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 9)

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
        self.deleted_forum3 = Forum.objects.create(forum_name="test_forum3", is_deleted=True)

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

        create_data = {
            "forum": self.forum1.id,
            "author_uuid": self.user_uuid,
            "title": "test_title5",
            "content": "test_content5"
        }
        response = self.client.post(self.url, data=create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Post.objects.all()), 5)

        edit_data_title = {
            "title": "new_title"
        }
        response = self.client.patch(self.url + f"{post1.id}/", data=edit_data_title)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "new_title")

        edit_data_forum = {
            "content": "new_content",
        }
        response = self.client.patch(self.url + f"{post1.id}/", data=edit_data_forum)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["content"], "new_content")

    def test_post_fail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        no_forum_data = {
            "author_uuid": self.user_uuid,
            "title": "test_title5",
            "content": "test_content5"
        }
        response = self.client.post(self.url, data=no_forum_data)
        self.assertEqual(response.status_code, 400)

        deleted_forum_data = {
            "forum": self.deleted_forum3.id,
            "author_uuid": self.user_uuid,
            "title": "test_title5",
            "content": "test_content5"
        }
        response = self.client.post(self.url, data=deleted_forum_data)
        self.assertEqual(response.status_code, 400)

        post = Post.objects.create(
            forum=self.forum1,
            author_uuid=self.user_uuid,
            title="test_title1",
            content="test_content1"
        )

        response = self.client.patch(self.url + f"{post.id}/", data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url + f"{post.id}/", data={"forum": self.forum2.id})
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url + f"{post.id}/", data={"author_uuid": uuid.uuid4()})
        self.assertEqual(response.status_code, 400)

class ReportLikeTestCase(APITestCase):
    def setUp(self):
        self.user_uuid = uuid.uuid4()
        self.forum1 = Forum.objects.create(forum_name="test_forum1")
        self.post1 = Post.objects.create(
            forum=self.forum1,
            author_uuid=self.user_uuid,
            title="test_title1",
            content="test_content1"
        )
        self.data = {
            "report_user_uuid": self.user_uuid,
            "report_content": "test_report_content",
            "report_reason": ReportReason.OTHER
        }
        self.comment1 = Comment.objects.create(
            post=self.post1,
            author_uuid=self.user_uuid,
            content="test_comment1"
        )
        self.recomment1 = ReComment.objects.create(
            comment=self.comment1,
            author_uuid=self.user_uuid,
            content="test_recomment1"
        )

    def test_report(self):
        post_report_data = {
            "post": self.post1.id,
            **self.data
        }
        response = self.client.post(
            "/api/posts/"+ f"{self.post1.id}/report/",
            data=post_report_data
        )
        self.assertEqual(response.status_code, 200)

        comment_report_data = {
            "comment": self.comment1.id,
            **self.data
        }
        response = self.client.post(
            "/api/comments/"+ f"{self.comment1.id}/report/",
            data=comment_report_data
        )
        self.assertEqual(response.status_code, 200)

        recomment_report_data = {
            "recomment": self.recomment1.id,
            **self.data
        }
        response = self.client.post(
            "/api/recomments/"+ f"{self.recomment1.id}/report/",
            data=recomment_report_data
        )
        self.assertEqual(response.status_code, 200)

    def test_report_fail(self):
        response = self.client.post("/api/posts/"+ f"{self.post1.id}/report/", data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/comments/"+ f"{self.comment1.id}/report/", data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/recomments/"+ f"{self.recomment1.id}/report/", data={})
        self.assertEqual(response.status_code, 400)

    def test_like(self):
        post_like_data = {
            "post": self.post1.id,
            "like_user_uuid": self.user_uuid
        }
        response = self.client.post(
            "/api/posts/"+ f"{self.post1.id}/like/",
            data=post_like_data
        )
        self.assertEqual(response.status_code, 200)

        comment_like_data = {
            "comment": self.comment1.id,
            "like_user_uuid": self.user_uuid
        }
        response = self.client.post(
            "/api/comments/"+ f"{self.comment1.id}/like/",
            data=comment_like_data
        )
        self.assertEqual(response.status_code, 200)

        recomment_like_data = {
            "recomment": self.recomment1.id,
            "like_user_uuid": self.user_uuid
        }
        response = self.client.post(
            "/api/recomments/"+ f"{self.recomment1.id}/like/",
            data=recomment_like_data
        )
        self.assertEqual(response.status_code, 200)

    def test_like_fail(self):
        response = self.client.post("/api/posts/"+ f"{self.post1.id}/like/", data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/comments/"+ f"{self.comment1.id}/like/", data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/api/recomments/"+ f"{self.recomment1.id}/like/", data={})
        self.assertEqual(response.status_code, 400)
