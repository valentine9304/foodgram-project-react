from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """ "Права для автора комментария или администратора."""

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_superuser
            or request.user.is_staff
            or request.user.role == "admin"
        )


class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """Предоставляет права только Пользователю или Админам."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.id == request.user
            or request.user.is_superuser
            or request.user.is_staff
            or request.user.role == "admin"
        )
