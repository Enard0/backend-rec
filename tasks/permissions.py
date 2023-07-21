from rest_framework.permissions import BasePermission

NOT_AUTH_METHODS = ('POST', 'HEAD', 'OPTIONS')
AUTH_METHODS = ('GET')
SUPERUSER_METHODS = ('DELETE')
REGISTER_METHODS = ('GET','POST', 'HEAD', 'OPTIONS')

class UserPerms(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in NOT_AUTH_METHODS or \
            request.user and request.user.is_authenticated and (
            request.method in AUTH_METHODS or
            request.user.is_superuser and request.method in SUPERUSER_METHODS))
            
class RegisterPerms(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in REGISTER_METHODS)