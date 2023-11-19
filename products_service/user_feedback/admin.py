from django.contrib import admin

from .models import CoachReview, CoachLike, FacilityReview, FacilityLike

admin.register(CoachReview)
admin.register(CoachLike)
admin.register(FacilityReview)
admin.register(FacilityLike)
