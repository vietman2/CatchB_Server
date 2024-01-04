from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='users'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.TokenView.as_view(), name='refresh_token'),
]
