from django.db import models

class BankAccount(models.Model):
    holder_name     = models.CharField(max_length=30, db_comment="예금주명")
    bank            = models.ForeignKey("Bank", on_delete=models.PROTECT, db_comment="은행")
    account_number  = models.CharField(unique=True, max_length=30, db_comment="계좌번호")
    branch_code     = models.CharField(null=True, max_length=3, db_comment="지점코드")

    is_verified     = models.BooleanField(default=False, db_comment="계좌인증여부")
    created_at      = models.DateTimeField(auto_now_add=True, db_comment="생성일시")
    updated_at      = models.DateTimeField(auto_now=True, db_comment="수정일시")

    class Meta:
        abstract = True

class UserBankAccount(BankAccount):
    user_uuid       = models.UUIDField(db_comment="사용자UUID")

    objects = models.Manager()

    class Meta:
        db_table = "user_bank_account"
        verbose_name = "사용자 은행계좌"
        verbose_name_plural = "사용자 은행계좌"

class CoachBankAccount(BankAccount):
    user_uuid       = models.UUIDField(db_comment="사용자UUID")
    coach_uuid      = models.UUIDField(db_comment="코치UUID")

    objects = models.Manager()

    class Meta:
        db_table = "coach_bank_account"
        verbose_name = "코치 은행계좌"
        verbose_name_plural = "코치 은행계좌"

class OwnerBankAccount(BankAccount):
    facility_uuid   = models.UUIDField(db_comment="아카데미UUID")

    objects = models.Manager()

    class Meta:
        db_table = "owner_bank_account"
        verbose_name = "사업자 은행계좌"
        verbose_name_plural = "사업자 은행계좌"

class Bank(models.Model):
    cms_code    = models.CharField(primary_key=True, max_length=3, db_comment="금융결제원코드")
    name        = models.CharField(max_length=30, db_comment="은행명")
    kor_code    = models.CharField(unique=True, max_length=4, db_comment="한국은행코드")
    eng_code    = models.CharField(unique=True, max_length=14, db_comment="영문은행코드")

    ## TODO: Add Images For Each Bank
    ##image       = models.ImageField(upload_to="bank_images", db_comment="은행 이미지")

    objects = models.Manager()

    class Meta:
        db_table = "bank"
        verbose_name = "은행"
        verbose_name_plural = "은행"
