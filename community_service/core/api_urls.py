from rest_framework.routers import DefaultRouter

from comment.views import CommentViewSet
from post.views import TagViewSet, ImageViewSet, PostViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tag')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
