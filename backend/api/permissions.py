from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_authenticated and obj.author == request.user)
            or request.method in permissions.SAFE_METHODS
        )


class IsAuthenticatedOrAdminOrReadOnlyMeSpecial(permissions.BasePermission):
    def has_permission(self, request, view):
        if "me" in request.path.split("/"):
            return request.user.is_authenticated
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if "me" in request.path.split("/"):
            return request.user.is_authenticated
        return request.method in SAFE_METHODS or request.user.is_authenticated
