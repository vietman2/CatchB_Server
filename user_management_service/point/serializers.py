from rest_framework import serializers

from .models import UserPoints, PointsEarnDetails, PointsUseDetails

class EarnPointsSerizlier(serializers.ModelSerializer):
    total_remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_total_remaining_points(self, obj):
        return UserPoints.objects.total_points(obj["user"].uuid)

    class Meta:
        model = PointsEarnDetails
        fields = [
            "user",
            "points",
            "title",
            "description",
            "valid_days",
            "total_remaining_points",
        ]

    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("point must be positive.")
        return value

    def save(self, **kwargs):
        UserPoints.objects.earn_points(**self.validated_data)
        return self.validated_data

class UsePointsSerializer(serializers.ModelSerializer):
    total_remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_total_remaining_points(self, obj):
        return UserPoints.objects.total_points(obj["user"].uuid)

    class Meta:
        model = PointsUseDetails
        fields = [
            "user",
            "points",
            "title",
            "description",
            "total_remaining_points",
        ]

    def validate_points(self, value):
        if value < 0:
            raise serializers.ValidationError("point must be positive.")
        return value

    # pylint: disable=W0221
    def update(self, validated_data):
        UserPoints.objects.use_points(**validated_data)

    def save(self, **kwargs):
        self.update(self.validated_data)
        return self.validated_data

class PointsDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    remaining_points = serializers.SerializerMethodField(read_only=True)

    def get_remaining_points(self, obj):
        return obj.remaining_points

    class Meta:
        model = UserPoints
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
