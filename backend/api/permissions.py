from rest_framework import permissions


class IsAuthorIsAdminOrReadOnly(permissions.BasePermission):
    """Allow safe methods for unauthenticated users or all methods for admins
    and content owners.
    """


    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return (request.user.is_superuser
                    or obj.author == request.user)
        return False


class Block(permissions.BasePermission):
    """Block access for all users."""


    def has_permission(self, request, view):
        return False
