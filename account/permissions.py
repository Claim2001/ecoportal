from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from account.models import ProfileModel


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False
