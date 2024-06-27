from rest_framework.permissions import BasePermission

from .or_read import or_read


class EmailVerifiedOrReadOnly(BasePermission):
    @or_read
    def has_permission(self, request, view):
        return request.user.email_verified
