from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('token/refresh/', views.refresh_token, name='refresh_token'),
    path('<str:uuid>/', views.get_user_profile, name='get_user_profile')
]
