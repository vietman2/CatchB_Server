from django.db.models import TextChoices

class CouponStatus(TextChoices):
    ACTIVE      = 'ACT', "사용 가능"
    USED        = 'USE', "사용 완료"
    EXPIRED     = 'EXP', "기한 만료"

class CouponIssuerType(TextChoices):
    CATCH_B     = 'CAT', "캐치비"
    FACILITY    = 'FAC', "시설"
    COACH       = 'COA', "코치"
    NULL        = 'NUL', "없음"

class CouponType(TextChoices):
    PERCENTAGE  = 'PCNT', "할인율"
    AMOUNT      = 'AMNT', "금액"
    FREE        = 'FREE', "무료"
