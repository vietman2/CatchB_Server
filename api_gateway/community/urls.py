from django.urls import path

from . import views

urlpatterns = [
    path("tags/", views.TagView.as_view(), name="forums"),
    path("images/", views.ImageView.as_view(), name="images"),
    path("posts/", views.PostView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("comments/", views.CommentView.as_view(), name="comments"),
]
