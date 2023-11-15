import uuid
from django.db import models

class LessonProduct(models.Model):
    title           = models.CharField(max_length=100, null=False, blank=False, db_comment="상품명")
    description     = models.TextField(null=False, blank=False, db_comment="상품 설명")
    price           = models.IntegerField(null=False, db_comment="가격")
    main_coach      = models.UUIDField(null=False, db_comment="코치 고유번호")

    num_sessions    = models.IntegerField(null=False, db_comment="세션 수")
    num_finished    = models.IntegerField(default=0, null=False, db_comment="완료된 세션 수")
    num_booked      = models.IntegerField(default=0, null=False, db_comment="예약된 세션 수")

    class Meta:
        db_table = "lesson_product"
        verbose_name = "레슨 상품"
        verbose_name_plural = "레슨 상품"

class Status(models.TextChoices):
    PENDING     = "PE", "대기중"
    CONFIRMED   = "CO", "예약승인됨"
    CANCELED    = "CA", "취소됨"
    FINISHED    = "FI", "완료됨"

class LessonSession(models.Model):
    uuid            = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="세션 고유번호"
    )
    product         = models.ForeignKey(
        "LessonProduct",
        on_delete=models.DO_NOTHING,
        db_comment="레슨 상품 고유번호",
    )
    sub_coaches     = models.JSONField(null=True, db_comment="보조 코치 고유번호 배열")
    reserved_user   = models.UUIDField(null=False, db_comment="사용자 고유번호")

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

class Stars(models.IntegerChoices):
    ONE     = 1, "1"
    TWO     = 2, "2"
    THREE   = 3, "3"
    FOUR    = 4, "4"
    FIVE    = 5, "5"

class LessonReview(models.Model):
    ## 리뷰는 사용자가 시설에 대해 남긴다
    lesson      = models.UUIDField(null=False, blank=False, db_comment="레슨 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")
    content     = models.TextField(null=False, blank=False, db_comment="내용")
    content_open= models.BooleanField(default=False, db_comment="내용 공개 여부")
    images      = models.JSONField(null=True, blank=True, db_comment="이미지 URL 배열")
    stars       = models.IntegerField(
        choices=Stars.choices,
        db_comment="별점",
        null=False,
        blank=False
    )

    class Meta:
        db_table = "lesson_review"
        indexes = [
            #TODO: 코치에 대한 인덱스 추가
            models.Index(fields=["user"], name="lesson_review_user_index"),
        ]
        verbose_name = "레슨 리뷰"
        verbose_name_plural = "레슨 리뷰"
