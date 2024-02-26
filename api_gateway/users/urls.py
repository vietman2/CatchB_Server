from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('token/refresh/', views.TokenView.as_view(), name='refresh_token'),
    path('coupons/', views.CouponView.as_view(), name='coupons'),
    path('coupons/register/', views.CouponRegisterView.as_view(), name='coupons'),
    path('coupons/status/', views.CouponStatusCheckView.as_view(), name='coupons_status'),
    path('points/', views.PointsView.as_view(), name='points'),
    path('<str:uuid>/', views.UserView.as_view(), name='users'),
]
