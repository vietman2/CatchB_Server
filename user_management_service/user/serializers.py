from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DNEError
from django.utils.encoding import force_str
from dj_rest_auth.forms import AllAuthPasswordResetForm
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from drf_spectacular.utils import extend_schema_field
from allauth.account.forms import default_token_generator
from allauth.account.utils import url_str_to_user_pk as uid_decoder

from .models import CustomUser, Coach

class UserRegisterSerializer(ModelSerializer):
    """
    회원가입 시리얼라이저
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "password2",
            "gender",
            "register_route"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate_passwords(self, value):
        if value["password"] != value["password2"]:
            raise serializers.ValidationError({"password": ["비밀번호가 일치하지 않습니다."]})
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def save(self, **kwargs):
        self.create(self.validated_data)
        return self.validated_data

class UserSerializer(ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    experience_tier = serializers.CharField(source="get_experience_tier_display")
    register_route = serializers.CharField(source="get_register_route_display")
    user_type = serializers.SerializerMethodField()
    num_coupons = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_phone_number(self, obj):
        return obj.phone_number.as_national

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        return obj.full_name

    @extend_schema_field(serializers.IntegerField())
    def get_num_coupons(self, obj):
        return obj.user_coupons.count()

    @extend_schema_field(serializers.CharField())
    def get_total_points(self, obj):
        points = obj.user_points.all()
        total_points = 0
        for point_obj in points:
            total_points += point_obj.remaining_points

        # format: , every 3 digits
        return format(total_points, ',')

    class Meta:
        model = CustomUser
        fields = [
            "uuid",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "date_joined",
            'nickname',
            "birth_date",
            "gender",
            "experience_tier",
            "register_route",
            "user_type",
            'num_coupons',
            'total_points',
        ]

    def validate_username(self, value):
        raise serializers.ValidationError("username은 수정할 수 없습니다.")

    def get_user_type(self, obj):
        ## Coach 인스턴스가 존재하면 코치
        if hasattr(obj, "coach"):
            return "coach"
        if obj.is_facility_owner:
            return "facility_owner"
        if obj.is_superuser:
            return "admin"

        return "normal_user"

class CoachProfileSerializer(ModelSerializer):
    """
    코치 프로필 시리얼라이저: 코치가 자신의 프로필을 조회하거나 수정할 때 사용
    """
    class Meta:
        model = Coach
        fields = [
            # "user",
            # "profile",
            "academic_background",
            "baseball_career",
            "coaching_career",
        ]

class PasswordChangeSerializer(ModelSerializer):
    """
    비밀번호 변경 시리얼라이저: 로그인이 된 유저가 자신의 비밀번호를 변경할 때 사용
    """
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    set_password_form_class = SetPasswordForm

    set_password_form = None

    class Meta:
        model = CustomUser
        fields = [
            "old_password",
            "new_password1",
            "new_password2"
        ]
        extra_kwargs = {
            "old_password": {"write_only": True},
            "new_password1": {"write_only": True},
            "new_password2": {"write_only": True},
        }

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 일치하지 않습니다.")
        return value

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError("새로운 비밀번호가 일치하지 않습니다.")

        if attrs["old_password"] == attrs["new_password1"]:
            raise serializers.ValidationError("새로운 비밀번호가 기존 비밀번호와 일치합니다.")

        self.set_password_form = self.set_password_form_class(
            user=self.context["request"].user,
            data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self, **kwargs):
        self.set_password_form.save()
        self.set_password_form.user.refresh_from_db()
        return self.set_password_form.user

class PasswordResetSerializer(serializers.Serializer):
    """
    비밀번호 재설정 시리얼라이저: 비밀번호를 잊어버린 유저가 비밀번호를 이메일을 통해
        재설정 링크를 받아 새로운 비밀번호를 설정할 때 사용
    """
    email = serializers.EmailField()
    reset_form = AllAuthPasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.reset_form(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("가입되지 않은 이메일입니다.")
        if not CustomUser.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("탈퇴한 계정입니다.")

        return value

    def save(self, **kwargs):
        request = self.context["request"]

        opts = {
            "use_https": request.is_secure(),
            "token_generator": default_token_generator,
            "from_email": None,     # getattrs(settings, "DEFAULT_FROM_EMAIL"),
            "request": request,
        }

        self.reset_form.save(**opts)

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    비밀번호 재설정 확인 시리얼라이저: 비밀번호를 재설정할 때 사용
    """
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def validate(self, attrs):
        try:
            uid = force_str(uid_decoder(attrs["uid"]))
            self.user = CustomUser.objects.get(pk=uid)
        # catch error when user is not found
        except (TypeError, ValueError, OverflowError, DNEError) as exc:
            raise ValidationError({"uid": ["올바르지 않은 값입니다."]}) from exc

        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise ValidationError({"token": ["올바르지 않은 값입니다."]})

        self.set_password_form = self.set_password_form_class(user=self.user, data=attrs)

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self, **kwargs):
        self.set_password_form.save()
        self.set_password_form.user.refresh_from_db()
        return self.set_password_form.user
