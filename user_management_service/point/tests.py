import datetime
from rest_framework.test import APITestCase

from .models import Points, PointStatus
from user.models import CustomUser

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
        self.initialPoints = Points.objects.create(
            user=self.user,
            points=1000,
            used_points=0,
            status=PointStatus.ACTIVE,
            valid_until=datetime.datetime.now().astimezone(datetime.timezone.utc) + datetime.timedelta(days=30),
        )

    def test_unallowed_methods(self):
        # login first for authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, 405)

    def test_points_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            "user": self.user_uuid,
            "points": 1500,
            "used_points": 0,
            "status": PointStatus.ACTIVE,
            "valid_until": datetime.datetime.now() + datetime.timedelta(days=30),
        }, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(self.url, {
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(self.url + "total/", {
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 2500)

        response = self.client.get(self.url + str(self.initialPoints.id) + "/")
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 500,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 2000)

        response = self.client.get(self.url + "total/", {
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 2000)

        response = self.client.get(self.url + str(self.initialPoints.id) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["remaining_points"], 500)
        self.assertEqual(response.data["used_points"], 500)
        self.assertEqual(response.data["status"], "부분 사용")

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 1500,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 500)

        response = self.client.get(self.url + "total/", {
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 500)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 500,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_remaining_points"], 0)

        response = self.client.get(self.url, {
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 200)

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
            "user_uuid": self.user_uuid
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.url + "total/", {
            "user_uuid": self.user_uuid
        })

        response = self.client.get(self.url + str(self.initialPoints.id) + "/")
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 500,
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
            "user_uuid": "invalid_uuid"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url + "total/", {
            "user_uuid": "invalid_uuid"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url + "invalid_id/")
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(self.url + "use/", {
            "user": "invalid_uuid",
            "points": 500,
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
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_points_failure_not_enough_points(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url + "use/", {
            "user": self.user_uuid,
            "points": 1500,
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_points_no_user_uuid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url + "total/")
        self.assertEqual(response.status_code, 400)
