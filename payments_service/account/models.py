from django.db import models

class BankAccount(models.Model):
    holder_name     = models.CharField(max_length=30)
    bank            = models.ForeignKey("Bank", on_delete=models.PROTECT)
    account_number  = models.CharField(unique=True, max_length=30)
    branch_code     = models.CharField(blank=True, default="", max_length=3)

    is_verified     = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserBankAccount(BankAccount):
    user_uuid       = models.UUIDField()

    objects = models.Manager()

    class Meta:
        db_table = "user_bank_account"

class CoachBankAccount(BankAccount):
    user_uuid       = models.UUIDField()
    coach_uuid      = models.UUIDField()

    objects = models.Manager()

    class Meta:
        db_table = "coach_bank_account"

class OwnerBankAccount(BankAccount):
    facility_uuid   = models.UUIDField()

    objects = models.Manager()

    class Meta:
        db_table = "owner_bank_account"

class Bank(models.Model):
    cms_code    = models.CharField(primary_key=True, max_length=3)
    name        = models.CharField(max_length=30)
    kor_code    = models.CharField(unique=True, max_length=4)
    eng_code    = models.CharField(unique=True, max_length=14)

    icon        = models.URLField()

    objects = models.Manager()

    class Meta:
        db_table = "bank"
