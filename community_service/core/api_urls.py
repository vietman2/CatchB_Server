from rest_framework.routers import DefaultRouter

from post.views import TagViewSet, ImageViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tag')
router.register(r'images', ImageViewSet, basename='image')

urlpatterns = router.urls
