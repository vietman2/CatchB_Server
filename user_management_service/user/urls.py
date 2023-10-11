from django.urls import path
from dj_rest_auth.views import (
    LoginView, LogoutView,
    PasswordResetConfirmView, PasswordResetView
)

from .views import RegisterView, PasswordChangeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-change/", PasswordChangeView.as_view(), name="pw-change"),

    path("password-reset/", PasswordResetView.as_view(), name="pw-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="pw-reset-confirm"),
    # path("user/", )
]
