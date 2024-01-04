from rest_framework.test import APITestCase

from user.models import CustomUser
from .models import CouponClass
from .enums import CouponIssuerType, CouponType

class CouponTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/coupons/"
        self.user = CustomUser.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            phone_number="010-1234-5678",
            password="passpass1234",
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

    def test_coupon_success(self):
        self.client.force_authenticate(user=self.admin)

        ## create coupon class (쿠폰 발행)
        response = self.client.post(self.url, self.create_coupon_class_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_coupon_create_failure(self):
        # normal user cannot create coupon class
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.create_coupon_class_data, format="json")
        self.assertEqual(response.status_code, 403)
