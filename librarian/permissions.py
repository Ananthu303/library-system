from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from users.models import CustomUser


class CanManageBooks(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        if (
            request.user
            and request.user.is_authenticated
            and request.user.user_type
            in [CustomUser.UserType.SUPERADMIN, CustomUser.UserType.LIBRARIAN]
        ):
            return True

        if request.user and request.user.is_authenticated:
            raise PermissionDenied("Only SuperAdmin or Librarian can manage books.")

        return False
