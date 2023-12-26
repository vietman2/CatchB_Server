import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
from .enums import ExperienceTierChoices, RegisterRouteChoices
from .validators import CustomUsernameValidator

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = CustomUsernameValidator()
    min_length_validator = MinLengthValidator(4)

    uuid            = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    username        = models.CharField(
        max_length=20,
        unique=True,
        db_comment='아이디',
        help_text='Required. 4~20. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator, min_length_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    first_name      = models.CharField(max_length=50, db_comment='이름')
    last_name       = models.CharField(max_length=50, db_comment='성')
    email           = models.EmailField(unique=True, db_comment='이메일')
    phone_number    = PhoneNumberField(unique=True, db_comment='전화번호')

    date_joined     = models.DateTimeField(auto_now_add=True, db_comment='가입일')

    is_superuser    = models.BooleanField(
        default=False,
        db_comment='슈퍼유저 여부',
        help_text='Designates that this user has all permissions without '
                    'explicitly assigning them.',
    )
    is_active       = models.BooleanField(
        default=True,
        db_comment='계정 활성화 여부',
        help_text='Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.',
    )

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
    ]

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
        related_name='user_profile'
    )

    nickname = models.CharField(max_length=150, db_comment='닉네임', null=True, blank=True)
    birth_date = models.DateField(db_comment='생년월일', null=True, blank=True)
    gender = models.CharField(max_length=1, db_comment='성별', null=True, blank=True)

    ## region = models.IntegerField(choices=RegionChoices.choices, db_comment='지역')
    # baseball_experience = models.IntegerField(choices=CareerChoices.choices, db_comment='야구 경력')
    # profile_image_url = models.URLField(db_comment='프로필 이미지 URL')

    experience_tier = models.IntegerField(
        choices=ExperienceTierChoices.choices,
        db_comment='야구 경험 등급',
        default=ExperienceTierChoices.BEGINNER
    )

    register_route = models.IntegerField(
        choices=RegisterRouteChoices.choices,
        db_comment='가입 경로',
        default=RegisterRouteChoices.CATCHB
    )

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('user_profile')
        verbose_name_plural = _('user_profiles')

class Coach(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
        related_name='coach'
    )

    # certification = models.FileField(db_comment='자격증', help_text='자격증을 첨부해주세요.')
    academic_background = models.TextField(db_comment='학력', help_text='학력을 입력해주세요.')
    baseball_career = models.TextField(db_comment='야구 경력', help_text='야구 경력을 입력해주세요.')
    coaching_career = models.TextField(db_comment='코칭 경력', help_text='코칭 경력을 입력해주세요.')
    # facility = models.TextField(db_comment="소속 시설")
    # areas = models.TextField(db_comment="레슨 영역", help_text="레슨 영역: 타격, 투구, 수비, 주루, 트레이닝, 피지컬, 기타")

    is_approved = models.BooleanField(default=False, db_comment='코치 승인 여부')

    class Meta:
        db_table = 'coach'
        verbose_name = _('coach')
        verbose_name_plural = _('coaches')

class FacilityOwner(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
        related_name='facility_owner'
    )

    facility_name = models.CharField(max_length=150, db_comment='시설명')
    facility_address = models.CharField(max_length=150, db_comment='시설 주소')
    facility_phone_number = PhoneNumberField(db_comment='시설 전화번호')

    class Meta:
        db_table = 'facility_owner'
        verbose_name = _('facility_owner')
        verbose_name_plural = _('facility_owners')

class Partner(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
        related_name='partner'
    )

    class Meta:
        db_table = 'partner'
        verbose_name = _('partner')
        verbose_name_plural = _('partners')

class Counselor(CustomUser):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        parent_link=True,
        related_name='counselor'
    )

    class Meta:
        db_table = 'counselor'
        verbose_name = _('counselor')
        verbose_name_plural = _('counselors')
