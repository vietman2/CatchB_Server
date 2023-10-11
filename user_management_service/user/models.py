from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserTypeChoices(models.IntegerChoices):
        ADMIN = 0, '관리자'
        NORMAL = 1, '일반'
        COACH = 2, '코치'
        FACILITY_OWNER = 3, '시설주'
        PARTNER = 4, '파트너'
        COUNSELOR = 5, '상담사'
        GOODS_SELLER = 6, '용품판매자'
        FASHION_EDITOR = 7, '패션에디터'

    class RegisterRouteChoices(models.IntegerChoices):
        CATCHB = 0, '캐치비'
        KAKAO = 1, '카카오'
        NAVER = 2, '네이버'

    class ExperienceTierChoices(models.IntegerChoices):
        BEGINNER = 0, '초보'
        INTERMEDIATE = 1, '중급'
        ADVANCED = 2, '고급'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        db_comment='아이디',
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(max_length=150, db_comment='이름')
    last_name = models.CharField(max_length=150, db_comment='성')
    email = models.EmailField(db_comment='이메일')
    phone_number = PhoneNumberField(unique=True, db_comment='전화번호')

    birth_date = models.DateField(db_comment='생년월일', null=True, blank=True)
    gender = models.CharField(max_length=1, db_comment='성별', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_comment='가입일')

    experience_tier = models.IntegerField(
        choices=ExperienceTierChoices.choices,
        db_comment='야구 경험 등급',
        default=ExperienceTierChoices.BEGINNER
    )
    ## region = models.IntegerField(choices=RegionChoices.choices, db_comment='지역')
    # baseball_experience = models.IntegerField(choices=CareerChoices.choices, db_comment='야구 경력')
    # profile_image_url = models.URLField(db_comment='프로필 이미지 URL')

    is_staff = models.BooleanField(
        default=False,
        db_comment='스태프 여부',
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        db_comment='계정 활성화 여부',
        help_text='Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.',
    )

    user_type = models.IntegerField(
        choices=UserTypeChoices.choices,
        db_comment='유저 타입',
        default=UserTypeChoices.NORMAL
    )
    register_route = models.IntegerField(
        choices=RegisterRouteChoices.choices,
        db_comment='가입 경로',
        default=RegisterRouteChoices.CATCHB
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
    ]

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Coach(CustomUser):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True
    )

    academic_background = models.TextField(db_comment='학력', help_text='학력을 입력해주세요.')
    baseball_career = models.TextField(db_comment='야구 경력', help_text='야구 경력을 입력해주세요.')
    coaching_career = models.TextField(db_comment='코칭 경력', help_text='코칭 경력을 입력해주세요.')
    # facility = models.TextField(db_comment="소속 시설")
    # areas = models.TextField(db_comment="레슨 영역", help_text="레슨 영역: 타격, 투구, 수비, 주루, 트레이닝, 피지컬, 기타")

    class Meta:
        db_table = 'coach'
        verbose_name = _('coach')
        verbose_name_plural = _('coaches')

class FacilityOwner(CustomUser):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True
    )

    facility_name = models.CharField(max_length=150, db_comment='시설명')
    facility_address = models.CharField(max_length=150, db_comment='시설 주소')
    facility_phone_number = PhoneNumberField(db_comment='시설 전화번호')

    class Meta:
        db_table = 'facility_owner'
        verbose_name = _('facility_owner')
        verbose_name_plural = _('facility_owners')

class Partner(CustomUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, parent_link=True)

    class Meta:
        db_table = 'partner'
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

class Counselor(CustomUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, parent_link=True)

    class Meta:
        db_table = 'counselor'
        verbose_name = _('counselor')
        verbose_name_plural = _('counselors')
