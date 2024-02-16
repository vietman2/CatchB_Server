import datetime
from unittest.mock import patch, MagicMock
from django.utils import timezone
from rest_framework.test import APITestCase
from celery.result import AsyncResult

from user.models import CustomUser
from .models import Coupon, CouponClass
from .enums import CouponIssuerType, CouponType
from .tasks import process_register

class CouponAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/coupons/"
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
            is_active=True,
        )
        self.admin = CustomUser.objects.create_superuser(
            username="admin",
            first_name="admin",
            last_name="admin",
            email="admin@admin.com",
            phone_number="010-1234-4321",
            password="passpass1234",
        )
        self.sample_coupon_class = CouponClass.objects.create(
            coupon_name="test",
            coupon_description="test",
            coupon_issuer_type=CouponIssuerType.CATCH_B,
            coupon_issuer=self.admin,
            issue_valid_days=30,
            use_valid_days=30,
            max_count=100,
            coupon_type=CouponType.AMOUNT,
            discount_value=1000,
        )
        self.create_coupon_class_data = {
            "coupon_name": "test",
            "coupon_description": "test",
            "coupon_issuer_type": CouponIssuerType.CATCH_B,
            "coupon_issuer": self.admin.uuid,
            "issue_valid_days": 30,
            "use_valid_days": 30,
            "max_count": 100,
            "coupon_type": CouponType.AMOUNT,
            "discount_value": 1000,
        }

    def test_unallowed_methods(self):
        # login first for authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 405)

    def test_coupon_success(self):
        self.client.force_authenticate(user=self.admin)

        ## create coupon class (쿠폰 발행)
        response = self.client.post(self.url, self.create_coupon_class_data, format="json")
        self.assertEqual(response.status_code, 201)

        ## get coupon class list (쿠폰 목록 조회)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_coupon_create_failure(self):
        # invalid data
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_coupon_register_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url + "register/",
            {"coupon_code": self.sample_coupon_class.code},
            format="json"
        )
        self.assertEqual(response.status_code, 202)

    def test_coupon_register_failure(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url + "register/",
            {"coupon_code": "1234567890"},
            format="json"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(self.url + "register/", {"coupon_code": ""}, format="json")
        self.assertEqual(response.status_code, 400)

class CouponRegisterWorkerTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="email@email.com",
            phone_number="010-1234-5678",
            password="passpass1234",
            is_active=True,
        )
        self.admin = CustomUser.objects.create_superuser(
            username="admin",
            first_name="admin",
            last_name="admin",
            email="admin@admin.com",
            phone_number="010-1234-4321",
            password="passpass1234",
        )
        self.url = "/api/coupons/"
        self.sample_coupon_class = CouponClass.objects.create(
            coupon_name="test",
            coupon_description="test",
            coupon_issuer_type=CouponIssuerType.CATCH_B,
            coupon_issuer=self.admin,
            issue_valid_days=30,
            use_valid_days=30,
            max_count=1,
            coupon_type=CouponType.AMOUNT,
            discount_value=1000,
        )
        self.sample_coupon_class2 = CouponClass.objects.create(
            coupon_name="test",
            coupon_description="test",
            coupon_issuer_type=CouponIssuerType.CATCH_B,
            coupon_issuer=self.admin,
            issue_valid_days=30,
            use_valid_days=30,
            max_count=-1,
            coupon_type=CouponType.AMOUNT,
            discount_value=1000,
        )
        self.sample_coupon_class3 = CouponClass.objects.create(
            coupon_name="test",
            coupon_description="test",
            coupon_issuer_type=CouponIssuerType.CATCH_B,
            coupon_issuer=self.admin,
            issue_valid_days=30,
            use_valid_days=30,
            max_count=0,
            coupon_type=CouponType.AMOUNT,
            discount_value=1000,
        )

    @patch("coupon.tasks.process_register.delay")
    def test_register_worker(self, mock_process_register):  # pylint: disable=W0613
        request_datetime = datetime.datetime.now()
        aware_datetime = timezone.make_aware(request_datetime)

        process_register(
            user_uuid=self.user.pk,
            coupon_code=self.sample_coupon_class.code,
            request_datetime=aware_datetime
        )

        process_register(
            user_uuid=self.user.pk,
            coupon_code=self.sample_coupon_class2.code,
            request_datetime=aware_datetime
        )

    @patch("celery.result.AsyncResult.ready")
    def test_coupon_status_check_success(self, mock_ready):  # pylint: disable=W0613
        self.client.force_authenticate(user=self.user)

        mock_ready.return_value = True
        response = self.client.get(self.url + "status/", {"task_id": "task_id"})
        self.assertEqual(response.status_code, 200)

        mock_ready.return_value = False
        response = self.client.get(self.url + "status/", {"task_id": "task_id"})
        self.assertEqual(response.status_code, 202)

    def test_coupon_status_check_failure(self):
        self.client.force_authenticate(user=self.user)

        # no task id
        response = self.client.get(self.url + "status/", {"task_id": ""})
        self.assertEqual(response.status_code, 400)
