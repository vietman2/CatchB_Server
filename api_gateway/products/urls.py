from django.urls import path

from . import views

urlpatterns = [
    path('facilities/', views.FacilityView.as_view(), name='address'),
    path('facilities/<str:uuid>/', views.FacilityInfoView.as_view(), name='info'),
    path('regions/', views.RegionView.as_view(), name='regions'),
]
