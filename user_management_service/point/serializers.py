from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Points

class UserTotalPointsSerializer(serializers.Serializer):
    points = serializers.IntegerField()

class CreatePointsSerizlier(ModelSerializer):
    class Meta:
        model = Points
        fields = [
            "user",
            "points",
            "created_at",
            "status",
            "valid_until",
        ]

    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("point must be positive.")
        return value

    def create(self, validated_data):
        return Points.objects.create(**validated_data)
    
    def save(self, **kwargs):
        self.create(self.validated_data)
        return self.validated_data

class UsePointsSerializer(ModelSerializer):
    total_remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_total_remaining_points(self, obj):
        return Points.objects.total_points(obj["user"].uuid)

    class Meta:
        model = Points
        fields = [
            "user",
            "points",
            "total_remaining_points",
        ]

    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("point must be positive.")
        return value

    def update(self, validated_data):
        Points.objects.use_points(**validated_data)

    def save(self, **kwargs):
        self.update(self.validated_data)
        return self.validated_data

class PointsDetailSerializer(ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_remaining_points(self, obj):
        return obj.remaining_points

    class Meta:
        model = Points
        fields = [
            "id",
            "user",
            "points",
            "used_points",
            "remaining_points",
            "status",
            "created_at",
            "valid_until",
        ]
