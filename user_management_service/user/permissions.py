from rest_framework.permissions import BasePermission

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
