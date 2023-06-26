from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Просматривать/редактировать отзыв может только пользователь который его создал'

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user or request.method in permissions.SAFE_METHODS)


class CanAccessCartItems(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'update', 'partial_update']:
            return True
        return False
