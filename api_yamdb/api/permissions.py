from rest_framework.permissions import SAFE_METHODS, BasePermission


class ListAll_ModerAdminOnly(BasePermission):
    """
    Получение списка доступно всем пользователям.
    Модерирование доступно только администратору.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.user.is_superuser)


class IsAdminModerAuthorOrReadOnly(BasePermission):
    """Проверка авторизации и доступа к объектам"""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
