from django.db import models

# Create your models here.
class CustomUser(models.Model):
    # 관리자 (우리)
    # 일반유저 (일반유저 + 게스트)
    # 코치 (개인레슨코치 + 시설고용코치)
    # 시설업자
    # 파트너 (광고주 + 제휴업체)
    # 상담원

    #class UserType(models.TextChoices):
    #    ADMIN = "admin", "관리자"
    #    NORMAL = "normal", "일반유저"
    #    COACH = "coach", "코치"
    #    FACILITY_OWNER = "ownwer", "시설업자"

    ## 아래는 placeholder
    username = models.CharField(max_length=50)
