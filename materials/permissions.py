# materials/permissions.py
from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """Проверяет, является ли пользователь менеджером"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Managers").exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrManagerForEdit(BasePermission):
    """Разрешает доступ владельцам и менеджерам для редактирования"""

    def has_permission(self, request, view):
        # Разрешаем GET запросы всем
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return True  # Для остальных методов проверка на уровне объекта

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET запросы всем
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Для изменяющих запросов проверяем владельца или менеджера
        return (
            obj.owner == request.user
            or request.user.groups.filter(name="Managers").exists()
        )
