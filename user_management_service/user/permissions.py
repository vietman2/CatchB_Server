from rest_framework.permissions import BasePermission

class IsActive(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_active
