import datetime
from rest_framework.test import APITestCase


from user.models import CustomUser
from .models import UserPoints
from .enums import PointStatus

class PointsTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/points/"
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
        )
        self.user_uuid = self.user.uuid
        self.initial_points = UserPoints.objects.earn_points(
            user=self.user,
            points=1000,
            valid_days=10,
            title="test",
            description="test",
        )

    def test_unallowed_methods(self):
        # login first for authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 405)

    def test_points_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {
            "uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.post(self.url, {
            "user": self.user_uuid,
            "points": 500,
            "valid_days": 5,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 200,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 1300)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 800)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 800,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 0)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 0,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 0)

    def test_points_failure_unauthorized(self):
        # not logged in
        response = self.client.post(self.url, {
            "user": self.user_uuid,
            "points": 1500,
            "used_points": 0,
            "status": PointStatus.ACTIVE,
            "valid_until": datetime.datetime.now() + datetime.timedelta(days=30),
        }, format="json")
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.url, {
            "uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 403)

    def test_points_failure_invalid_user_uuid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            "user": "invalid_uuid",
            "points": 1500,
            "used_points": 0,
            "status": PointStatus.ACTIVE,
            "valid_until": datetime.datetime.now() + datetime.timedelta(days=30),
        }, format="json")
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url, {
            "uuid": "invalid_uuid"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url + "use/", {
            "user": "invalid_uuid",
            "points": 500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_points_failure_negative_points(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            "user": self.user_uuid,
            "points": -1500,
            "used_points": 0,
            "status": PointStatus.ACTIVE,
            "valid_until": datetime.datetime.now() + datetime.timedelta(days=30),
        }, format="json")
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": -500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_points_failure_not_enough_points(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 1500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_points_no_user_uuid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url, {
            "uuid": ""
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url + "use/", {
            "user": "invalid_uuid",
            "points": 500,
            "title": "test",
            "description": "test",
        }, format="json")
        self.assertEqual(response.status_code, 400)
