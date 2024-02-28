from django.db import models

class BankAccount(models.Model):
    holder_name     = models.CharField(max_length=30, db_comment="예금주명")
    account_number  = models.CharField(max_length=30, db_comment="계좌번호")
    bank_code       = models.CharField(max_length=3, db_comment="은행코드(금융결제원)")

    branch_code     = models.CharField(max_length=3, db_comment="지점코드")

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
