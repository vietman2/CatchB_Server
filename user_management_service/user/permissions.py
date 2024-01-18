from rest_framework.permissions import BasePermission

from .models import CustomUser

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        ## obj is uuid
        ## type of request.user.uuid is uuid.UUID, type of obj is str
        return str(request.user.uuid) == obj

class IsActive(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_active
    
class IsVerified(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_verified

class IsFacilityOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_facility_owner

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return CustomUser.objects.is_coach(request.user)
