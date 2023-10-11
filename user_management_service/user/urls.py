from django.urls import path
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetConfirmView, PasswordResetView
)

from .views import RegisterAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="pw-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="pw-reset-confirm"),
    path("password-change/", PasswordChangeView.as_view(), name="pw-change"),
    # path("user/", )
]
