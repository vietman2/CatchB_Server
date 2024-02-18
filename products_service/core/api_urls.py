from rest_framework.routers import DefaultRouter

from facility.views import FacilityViewSet
from lesson.views import LessonProductViewSet
from region.views import RegionViewSet

router = DefaultRouter()

router.register(r'facilities', FacilityViewSet, basename='facility')
router.register(r'lessons', LessonProductViewSet, basename='lesson')
router.register(r'regions', RegionViewSet, basename='region')

urlpatterns = router.urls
