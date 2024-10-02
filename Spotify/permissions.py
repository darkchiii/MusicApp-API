from rest_framework import permissions
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

"""Only owners can edit object, others can only read data."""
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

"""Only authenticated users can edit data, others can only read data."""
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or request.user and request.user.is_authenticated()):
            return True
        return False

"""Only owners can see and edit data."""
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False