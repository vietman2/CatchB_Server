import uuid
from django.db import models

class Status(models.TextChoices):
    WAITING     = "WA", "대기"
    CONFIRMED   = "CO", "승인"
    CANCELLED   = "CA", "취소"
    FINISHED    = "FI", "완료"

class ReservationProduct(models.Model):
    title           = models.CharField(max_length=100, null=False, blank=False, db_comment="상품명")
    description     = models.TextField(null=False, blank=False, db_comment="상품 설명")
    price           = models.IntegerField(null=False, db_comment="가격")
    facility        = models.UUIDField(null=False, db_comment="시설 고유번호")

    hours           = models.IntegerField(null=False, db_comment="시간")
    minutes         = models.IntegerField(null=False, db_comment="분")

    class Meta:
        db_table = "reservation_product"
        verbose_name = "예약 상품"
        verbose_name_plural = "예약 상품"

class Reservation(models.Model):
    uuid            = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="예약 고유번호"
    )
    product         = models.ForeignKey(
        "ReservationProduct",
        on_delete=models.DO_NOTHING,
        db_comment="예약 상품 고유번호",
    )
    reserved_user   = models.UUIDField(null=False, db_comment="사용자 고유번호")

    start_datetime  = models.DateTimeField(null=False, db_comment="시작 시간")
    end_datetime    = models.DateTimeField(null=False, db_comment="종료 시간")
    status          = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.WAITING,
        db_comment="예약 상태"
    )
    created_at      = models.DateTimeField(auto_now_add=True, db_comment="생성일")
    confirmed_at    = models.DateTimeField(null=True, blank=True, db_comment="승인일")

    class Meta:
        db_table = "reservation"
        ordering = ["start_datetime"]
        verbose_name = "예약"
        verbose_name_plural = "예약"
