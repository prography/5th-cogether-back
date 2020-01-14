from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsEmailloginUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.login_method == 'email')
