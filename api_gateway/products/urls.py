from django.urls import path

from . import views

urlpatterns = [
    path('coaches/', views.CoachView.as_view(), name='coach'),
    path('coaches/status/', views.CoachStatusView.as_view(), name='status'),
    path('coaches/<str:uuid>/', views.CoachInfoView.as_view(), name='coach_info'),
    path('facilities/', views.FacilityView.as_view(), name='facility'),
    path('facilities/status/', views.FacilityStatusView.as_view(), name='status'),
    path('facilities/<str:uuid>/', views.FacilityInfoView.as_view(), name='facility_info'),
    path('regions/', views.RegionView.as_view(), name='region'),
]
