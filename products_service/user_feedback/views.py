from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import CoachReview
#from .serializers import CoachReviewSerializer

class CoachReviewViewSet(ModelViewSet):
    queryset = CoachReview.objects.all()
    #serializer_class = CoachReviewSerializer
    permission_classes = [IsAuthenticated]
