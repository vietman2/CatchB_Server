import uuid
from django.db import models
from django.core.validators import MinLengthValidator as Min
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from .enums import ExperienceTierChoices, RegisterRouteChoices
from .managers import UserManager
from .validators import CustomUsernameValidator

class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid            = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    username        = models.CharField(
        max_length=20,
        unique=True,
        validators=[CustomUsernameValidator(), Min(4)],
    )
    first_name      = models.CharField(max_length=20)
    last_name       = models.CharField(max_length=20)
    email           = models.EmailField(unique=True)
    phone_number    = PhoneNumberField(unique=True)

    date_joined     = models.DateTimeField(auto_now_add=True)

    experience_tier = models.IntegerField(
        choices=ExperienceTierChoices.choices,
        default=ExperienceTierChoices.UNDEFINED
    )
    register_route = models.IntegerField(
        choices=RegisterRouteChoices.choices,
        default=RegisterRouteChoices.UNDEFINED
    )

    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    is_facility_owner = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        db_table = 'user'

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField(max_length=15)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)

    ## region = models.IntegerField(choices=RegionChoices.choices, db_comment='지역')
    # baseball_experience = models.IntegerField(choices=CareerChoices.choices, db_comment='야구 경력')
    # profile_image_url = models.URLField(db_comment='프로필 이미지 URL')
