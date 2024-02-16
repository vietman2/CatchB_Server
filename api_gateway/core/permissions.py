import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission

def get_user_info(request):
    token = request.headers.get('Authorization', None)

    if token is None:
        return None

    access = token.split(' ')[1]
    key = settings.PRIVATE_KEY

    if access is None:
        return None

    decoded = jwt.decode(access, key, algorithms='HS256')
    return decoded

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        return user_info['role'] == 'A'

class IsFacilityOwner(BasePermission):
    def has_permission(self, request, view):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        role = user_info['role']
        return role == 'F' or role == 'B'

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        role = user_info['role']
        return role == 'C' or role == 'B'

class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        return user_info['user_id'] == obj
