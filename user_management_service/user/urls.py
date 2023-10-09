from django.urls import path, include

from .views import RegisterAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    # path("api-auth/", include()"rest_framework.urls", namespace="rest_framework")),
    # path("change-password/", )
    # path("user/", )

]
