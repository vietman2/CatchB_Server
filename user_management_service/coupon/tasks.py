from __future__ import absolute_import, unicode_literals

from datetime import timedelta
from celery import shared_task
from django.db import IntegrityError

from user.models import CustomUser
from .models import Coupon, CouponClass

@shared_task(queue="coupon_queue")
def process_register(user_uuid, coupon_code, request_datetime):
    """
    쿠폰 다운로드 비동기 작업.
    """

    def calculate_valid_until(coupon_class_obj, request_datetime):
        """
        쿠폰 유효기간 계산.
        """
        days = coupon_class_obj.use_valid_days
        valid_until = request_datetime + timedelta(days=days)
        return valid_until

    try:
        coupon_class_obj = CouponClass.objects.get(code=coupon_code)

        if coupon_class_obj.max_count == -1:
            # 무제한 발급
            pass
        elif coupon_class_obj.max_count <= coupon_class_obj.current_count:
            return {
                "status": "error",
                "message": "쿠폰이 모두 소진되었습니다."
            }

        valid_date = calculate_valid_until(coupon_class_obj, request_datetime)

        user = CustomUser.objects.get(uuid=user_uuid)

        Coupon.objects.create(
            user=user,
            coupon_class=coupon_class_obj,
            issued_at=request_datetime,
            valid_until=valid_date
        )

        coupon_class_obj.current_count += 1
        coupon_class_obj.save()

        return {
            "status": "success",
            "message": "쿠폰이 생성되었습니다."
        }

    except IntegrityError:
        return {
            "status": "error",
            "message": "이미 등록된 쿠폰입니다."
        }
