from django.db import models

class Status(models.TextChoices):
    PENDING     = 'PEN', '대기'
    COMPLETED   = 'COM', '완료'
    CANCELLED   = 'CAN', '취소'
    FAILED      = 'FAL', '실패'

class PaymentMethod(models.TextChoices):
    CREDIT_CARD     = 'CREDIT_CARD', '신용카드'
    BANK_TRANSFER   = 'BANK_TRANSFER', '계좌이체'
    NAVER_PAY       = 'NAVER_PAY', '네이버페이'
    KAKAO_PAY       = 'KAKAO_PAY', '카카오페이'
    TOSS            = 'TOSS', '토스'
    PAYCO           = 'PAYCO', '페이코'
    SAMSUNG_PAY     = 'SAMSUNG_PAY', '삼성페이'

class Payment(models.Model):
    uuid        = models.UUIDField(primary_key=True)
    status      = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    price       = models.PositiveIntegerField(db_comment='결제 금액')

    buyer_uuid  = models.UUIDField(db_comment='구매자 uuid')
    seller_uuid = models.UUIDField(db_comment='판매자 uuid')    # TODO: 생각해보기

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class Refund(models.Model):
    uuid        = models.UUIDField(primary_key=True)
    payment     = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status      = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    price       = models.DecimalField(max_digits=10, decimal_places=2)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
