from rest_framework import serializers

from .models import Sido, Sigungu

class SidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sido
        fields = "__all__"

class SigunguSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Sigungu
        fields = ["code", "name"]

    def get_code(self, obj):
        return str(obj.sigungu_code)
    
    def get_name(self, obj):
        sido = obj.sido_code.sido_name
        return f"{sido} {obj.sigungu_name}"