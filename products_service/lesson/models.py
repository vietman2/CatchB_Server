import uuid
from django.db import models

class LessonProduct(models.Model):
    title           = models.CharField(max_length=100, null=False, blank=False, db_comment="상품명")
    description     = models.TextField(null=False, blank=False, db_comment="상품 설명")
    price           = models.IntegerField(null=False, db_comment="가격")
    main_coach      = models.UUIDField(null=False, db_comment="코치 고유번호")

    num_sessions    = models.IntegerField(null=False, db_comment="세션 수")

    deleted         = models.BooleanField(default=False, db_comment="삭제 여부")

    objects = models.Manager()

    class Meta:
        db_table = "lesson_product"
        verbose_name = "레슨 상품"
        verbose_name_plural = "레슨 상품"

class LessonPurchase(models.Model):
    product         = models.ForeignKey(
        "LessonProduct",
        on_delete=models.DO_NOTHING,
        db_comment="레슨 상품 고유번호",
    )
    sub_coaches     = models.JSONField(null=True, db_comment="보조 코치 고유번호 배열")
    user            = models.UUIDField(null=False, db_comment="사용자 고유번호")

    num_finished    = models.IntegerField(default=0, null=False, db_comment="완료된 세션 수")
    num_booked      = models.IntegerField(default=0, null=False, db_comment="예약된 세션 수")

    class Meta:
        db_table = "lesson_purchase"
        verbose_name = "레슨 구매"
        verbose_name_plural = "레슨 구매"

class Status(models.TextChoices):
    PENDING     = "PE", "대기"
    CONFIRMED   = "CO", "확정"
    CANCELLED    = "CA", "취소"
    FINISHED    = "FI", "완료"

class LessonSession(models.Model):
    uuid            = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="세션 고유번호"
    )
    purchase        = models.ForeignKey(
        "LessonPurchase",
        on_delete=models.DO_NOTHING,
        db_comment="레슨 구매 고유번호",
    )

    ## 팀이면 팀 정보

    start_datetime  = models.DateTimeField(null=False, db_comment="시작 날짜/시간")
    end_datetime    = models.DateTimeField(null=False, db_comment="종료 날짜/시간")
    status          = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
        db_comment="상태"
    )
    created_at      = models.DateTimeField(auto_now_add=True, db_comment="생성일")
    confirmed_at    = models.DateTimeField(null=True, blank=True, db_comment="승인일")

    class Meta:
        db_table = "lesson"
        verbose_name = "레슨"
        verbose_name_plural = "레슨"
