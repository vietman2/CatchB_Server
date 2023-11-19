from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from .models import Facility
from .serializers import FacilitySimpleSerializer

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySimpleSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @extend_schema(summary="시설 목록 조회", tags=["시설"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
