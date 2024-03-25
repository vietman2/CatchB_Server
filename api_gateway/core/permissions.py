import jwt
from jwt.exceptions import DecodeError
from django.conf import settings
from rest_framework.permissions import BasePermission

def get_user_info(request):
    token = request.headers.get('Authorization', None)
    key = settings.PRIVATE_KEY

    if token is None:
        return None

    try:
        access = token.split(' ')[1]

        decoded = jwt.decode(access, key, algorithms='HS256')
        return decoded
    except IndexError:
        return None
    except DecodeError:
        return None

class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        user_info = get_user_info(request)
        return user_info is not None

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
        return role in ['F', 'B']

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        role = user_info['role']
        return role in ['C', 'B']

class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_info = get_user_info(request)
        if user_info is None:
            return False

        return user_info['user_id'] == obj
