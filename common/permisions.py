from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Просматривать/редактировать отзыв может только пользователь который его создал'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
