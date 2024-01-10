from rest_framework import serializers

from .models import CouponClass, Coupon

class CouponClassSerializer(serializers.ModelSerializer):
    coupon_issuer_type = serializers.CharField(source="get_coupon_issuer_type_display")
    coupon_type = serializers.CharField(source="get_coupon_type_display")

    class Meta:
        model = CouponClass
        fields = [
            'code',
            'coupon_name',
            'coupon_description',
            'coupon_issuer_type',
            'coupon_issuer',
            'use_valid_days',
            'coupon_type',
            'discount_value',
        ]

class CouponClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponClass
        fields = [
            'coupon_name',
            'coupon_description',
            'coupon_issuer_type',
            'coupon_issuer',
            'issue_valid_days',
            'use_valid_days',
            'max_count',
            'coupon_type',
            'discount_value',
        ]

class CouponSerializer(serializers.ModelSerializer):
    coupon_class = CouponClassSerializer()

    class Meta:
        model = Coupon
        fields = '__all__'
        depth = 1
