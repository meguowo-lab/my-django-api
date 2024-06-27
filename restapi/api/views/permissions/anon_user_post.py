from rest_framework.permissions import BasePermission


class AnonUserPost(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        if request.user.is_anonymous:
            return True

        return False
