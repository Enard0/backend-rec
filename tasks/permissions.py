from rest_framework.permissions import BasePermission
from rest_framework.response import Response

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
    
def UserPermsDecorator(func):
    def wrappeer(*args, **kw):
        request=args[1]
        if  request.method in NOT_AUTH_METHODS or \
            request.user and request.user.is_authenticated and (
            request.method in AUTH_METHODS or
            request.user.is_superuser and request.method in SUPERUSER_METHODS):
                return func(*args, **kw)
        return Response([])
    return wrappeer