from django.urls import path

from . import views

urlpatterns = [
    path('', views.FacilityView.as_view(), name='address'),
]
