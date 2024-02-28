from django.urls import path

from . import views

urlpatterns = [
    path("banks/", views.BankView.as_view(), name="banks"),
]
