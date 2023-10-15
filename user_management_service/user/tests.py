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

    def test_unallowed_method(self):
        response = self.client.get("/api/account/register/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put("/api/account/register/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch("/api/account/register/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete("/api/account/register/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_success(self):
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "test")

        # 비밀번호가 암호화되어 저장되었는지 확인
        self.assertNotEqual(CustomUser.objects.get().password, "passpass1234")

        # 디폴트 값들이 잘 들어갔는지 확인
        self.assertEqual(CustomUser.objects.get().is_active, True)
        self.assertEqual(CustomUser.objects.get().is_superuser, False)
        self.assertEqual(CustomUser.objects.get().register_route, 0)
        self.assertEqual(CustomUser.objects.get().birth_date, None)
        self.assertEqual(CustomUser.objects.get().experience_tier, 0)

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
        self.assertEqual(CustomUser.objects.get().is_superuser, True)

    def test_register_fail_unique(self):
        # 1. username is not unique
        # 2. phone_number is not unique
        # 3. email is not unique
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
        self.data["password"] = "test"
        self.data["password2"] = "test"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. password is too common
        self.data["password"] = "password"
        self.data["password2"] = "password"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. password is entirely numeric
        self.data["password"] = "1234567890"
        self.data["password2"] = "1234567890"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 5. password is too similar to the username / email
        self.data["password"] = "test1234"
        self.data["password2"] = "test1234"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 6. password is too similar to the phone_number
        self.data["password"] = "01012345678"
        self.data["password2"] = "01012345678"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_email(self):
        # 1. email is not valid
        self.data["email"] = "test"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_username_validation(self):
        # 1. username is too long
        self.data["username"] = "verylong1234verylong1234verylong1234 \
                                    verylong1234verylong1234verylong1234 \
                                    verylong1234verylong1234verylong1234 \
                                    verylong1234verylong1234verylong1234verylong1234"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. username is not valid
        self.data["username"] = "test!"
        response = self.client.post("/api/account/register/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_fail_emptyfields(self):
        response = self.client.post("/api/account/register/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("/api/account/register/", data={"username": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "test",
            "password": "passpass1234",
        }
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
        )

    def test_unallowed_method(self):
        response = self.client.get("/api/account/login/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put("/api/account/login/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch("/api/account/login/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete("/api/account/login/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_success(self):
        response = self.client.post("/api/account/login/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "test")
        self.assertEqual(response.data["user"]["first_name"], "test")

        # check if token is created
        self.assertTrue(response.data["access"])

    def test_login_fail(self):
        # 1. username is not valid
        self.data["username"] = "test1"
        response = self.client.post("/api/account/login/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. password is not valid
        self.data["username"] = "test"
        self.data["password"] = "test"
        response = self.client.post("/api/account/login/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. user is not active
        self.user.is_active = False
        self.user.save()
        response = self.client.post("/api/account/login/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. empty fields
        response = self.client.post("/api/account/login/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("/api/account/login/", data={"username": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LogoutAPITestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "test",
            "password": "passpass1234",
        }
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
        )

    def test_unallowed_method(self):
        response = self.client.get("/api/account/logout/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put("/api/account/logout/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch("/api/account/logout/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete("/api/account/logout/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_logout_success(self):
        response = self.client.post("/api/account/login/", data=self.data)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post("/api/account/logout/", data={"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_fail(self):
        response = self.client.post("/api/account/login/", data=self.data)

        # 1. token is not valid
        response = self.client.post("/api/account/logout/", data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/api/account/logout/", data={"refresh": "test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PasswordChangeAPITestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "test",
            "password": "passpass1234",
        }
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
        )
        self.change_data = {
            "old_password": "passpass1234",
            "new_password1": "newpass1234",
            "new_password2": "newpass1234",
        }

    def test_unallowed_method(self):
        response = self.client.get("/api/account/password-change/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put("/api/account/password-change/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch("/api/account/password-change/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete("/api/account/password-change/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_password_change_success(self):
        response = self.client.post("/api/account/login/", data=self.data)
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # check old password
        self.assertTrue(self.user.check_password("passpass1234"))

        # 1. password is changed
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # new password is saved in db
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass1234"))

    def test_password_change_fail(self):
        response = self.client.post("/api/account/login/", data=self.data)
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 1. old password is not valid
        self.change_data["old_password"] = "wrongpassword"
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. old password is same as new password
        self.change_data["old_password"] = "passpass1234"
        self.change_data["new_password1"] = "passpass1234"
        self.change_data["new_password2"] = "passpass1234"
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. new password 1 and 2 are not matched
        self.change_data["new_password1"] = "newpass1234"
        self.change_data["new_password2"] = "newpass12345"
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. new password is not valid (too short)
        self.change_data["new_password1"] = "test"
        self.change_data["new_password2"] = "test"
        response = self.client.post("/api/account/password-change/", data=self.change_data)

        # 5. empty fields
        response = self.client.post("/api/account/password-change/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("/api/account/password-change/", data={"old_password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_fail_2(self):
        # 1. user is not authenticated
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 2. user with random token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.data["password"]}')
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 3. user is not active
        self.user.is_active = False
        self.user.save()
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_password_change_fail_3(self):
        # 1. user is not logged in
        response = self.client.post("/api/account/login/", data=self.data)
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.client.logout()
        response = self.client.post("/api/account/password-change/", data=self.change_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PasswordResetAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
        )

    def test_unallowed_method(self):
        response = self.client.get("/api/account/password/reset/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put("/api/account/password/reset/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch("/api/account/password/reset/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete("/api/account/password/reset/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_password_reset_success(self):
        # 1. password is reset
        response = self.client.post("/api/account/password/reset/", data={"email": "test@test.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_fail(self):
        # 1. user is not found
        response = self.client.post(
            "/api/account/password/reset/",
            data={"email": "wrong@email.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. email is not valid
        response = self.client.post("/api/account/password/reset/", data={"email": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. empty fields
        response = self.client.post("/api/account/password/reset/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. user is not active
        self.user.is_active = False
        self.user.save()
        response = self.client.post("/api/account/password/reset/", data={"email": "test@test.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
