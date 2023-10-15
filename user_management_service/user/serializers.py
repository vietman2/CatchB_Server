from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.forms import AllAuthPasswordResetForm
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUser

class UserRegisterSerializer(ModelSerializer):
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
            "password2"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate_passwords(self, value):
        if value["password"] != value["password2"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
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

class PasswordChangeSerializer(ModelSerializer):
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
    email = serializers.EmailField()
    reset_form = AllAuthPasswordResetForm

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("가입되지 않은 이메일입니다.")
        if not CustomUser.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("탈퇴한 계정입니다.")
        self.reset_form = self.reset_form(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

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

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
