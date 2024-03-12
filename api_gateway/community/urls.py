from django.urls import path

from . import views

urlpatterns = [
    path("tags/", views.TagView.as_view(), name="forums"),
    path("images/", views.ImageView.as_view(), name="images"),
]
