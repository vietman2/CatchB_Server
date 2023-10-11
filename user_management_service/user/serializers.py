from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password
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
