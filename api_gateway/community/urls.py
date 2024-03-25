from django.urls import path

from . import views

urlpatterns = [
    path("tags/", views.TagView.as_view(), name="forums"),
    path("images/", views.ImageView.as_view(), name="images"),
    path("posts/", views.PostView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/like/", views.PostLikeView.as_view(), name="post_like"),
    path("posts/<int:pk>/dislike/", views.PostDislikeView.as_view(), name="post_dislike"),
    path("comments/", views.CommentView.as_view(), name="comments"),
]
