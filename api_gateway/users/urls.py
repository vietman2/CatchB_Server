from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', views.refresh_token, name='refresh_token'),
    path('<str:uuid>/', views.get_user_profile, name='get_user_profile')
]
