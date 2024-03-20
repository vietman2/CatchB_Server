from rest_framework.routers import DefaultRouter

from coach.views import CoachViewSet
from facility.views import FacilityViewSet      ## pylint: disable=no-name-in-module
from lesson.views import LessonProductViewSet
from region.views import RegionViewSet

router = DefaultRouter()

router.register(r'coaches', CoachViewSet, basename='coach')
router.register(r'facilities', FacilityViewSet, basename='facility')
router.register(r'lessons', LessonProductViewSet, basename='lesson')
router.register(r'regions', RegionViewSet, basename='region')

urlpatterns = router.urls
