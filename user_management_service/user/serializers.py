from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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
            "username": {"validators": [UniqueValidator(queryset=CustomUser.objects.all())]},
            "phone_number": {"validators": [UniqueValidator(queryset=CustomUser.objects.all())]},
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
