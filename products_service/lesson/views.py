from rest_framework.viewsets import ModelViewSet

from .models import LessonProduct
from .serializers import LessonProductSerializer

class LessonProductViewSet(ModelViewSet):
    queryset = LessonProduct.objects.all()
    serializer_class = LessonProductSerializer
    http_method_names = ["get", "post", "patch", "delete"]
