from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField

from .models import CustomUser

class UserRegisterSerializer(ModelSerializer):
    phone_number = PhoneNumberField(required=True, allow_null=False, allow_blank=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "birth_date",
            "gender",
            "experience_tier",
        ]
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
