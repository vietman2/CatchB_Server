from rest_framework.test import APITestCase
from rest_framework import status
from django.core.management import call_command

from .models import CustomUser

class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "010-1234-5678",
            "password": "passpass1234",
            "password2": "passpass1234",
        }
        self.too_short = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "010-1234-5678",
            "password": "pass",
            "password2": "pass",
        }
        self.too_common = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "phone_number": "010-1234-5678",
            "password": "password",
            "password2": "password",
        }

    def test_register_success(self):
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "test")

    def test_register_success_superuser(self):
        call_command(
            "createsuperuser",
            username="admin",
            first_name="admin",
            last_name="admin",
            email="admin@test.com",
            phone_number="010-1234-1234",
            interactive=False,
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "admin")

    def test_register_fail_unique(self):
        # 1. username is not unique
        # 2. phone_number is not unique
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_password(self):
        # 1. password is not matched
        self.data["password2"] = "test1"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. password is too short
        response = self.client.post("/api/account/register/", data=self.too_short)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 3. password is too common
        response = self.client.post("/api/account/register/", data=self.too_common)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 4. password is entirely numeric
        # 5. password is too similar to the username
        # 6. password is too similar to the email
        # 7. password is too similar to the phone_number
        # 8. password contains invalid characters
