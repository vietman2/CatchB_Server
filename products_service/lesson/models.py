import uuid
from django.db import models

class LessonProduct(models.Model):
    title           = models.CharField(max_length=30)
    description     = models.TextField()
    price           = models.IntegerField()
    main_coach      = models.UUIDField(editable=False)

    num_sessions    = models.IntegerField()

    deleted         = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "lesson_product"

class LessonPurchase(models.Model):
    product         = models.ForeignKey(
        "LessonProduct",
        on_delete=models.DO_NOTHING
    )
    sub_coaches     = models.JSONField(null=True)
    user            = models.UUIDField(null=False)

    num_finished    = models.IntegerField(default=0, null=False)
    num_booked      = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = "lesson_purchase"

class Status(models.TextChoices):
    PENDING     = "PE", "대기"
    CONFIRMED   = "CO", "확정"
    CANCELLED    = "CA", "취소"
    FINISHED    = "FI", "완료"

class LessonSession(models.Model):
    uuid            = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    purchase        = models.ForeignKey(
        "LessonPurchase",
        on_delete=models.DO_NOTHING
    )

    ## 팀이면 팀 정보

    start_datetime  = models.DateTimeField(null=False)
    end_datetime    = models.DateTimeField(null=False)
    status          = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    confirmed_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "lesson"
