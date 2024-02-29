from rest_framework import serializers

from .models import Sido, Sigungu

class SidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sido
        fields = "__all__"

class SigunguSerializer(serializers.ModelSerializer):
    code    = serializers.SerializerMethodField()
    name    = serializers.SerializerMethodField()
    label   = serializers.SerializerMethodField()

    class Meta:
        model = Sigungu
        fields = ["code", "name", "label"]

    def get_code(self, obj):
        return str(obj.sigungu_code)

    def get_name(self, obj):
        sido = obj.sido.label
        return f"{sido} {obj.sigungu_name}"
    
    def get_label(self, obj):
        return obj.sigungu_name
