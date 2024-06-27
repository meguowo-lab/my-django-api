from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.request import Request

from .or_read import or_read


def same_user(user_attr: str | None = None):
    class SameUserOrReadOnly(BasePermission):
        @or_read
        def has_object_permission(self, request, view, obj):
            if user_attr is None:
                if obj == request.user:
                    return True
            elif obj.__getattribute__(user_attr) == request.user:
                return True

            return False

        @or_read
        def has_permission(self, request: Request, view):
            if len(view.kwargs) == 0:
                return True

            if request.user.id == int(view.kwargs["pk"]):
                return True

            return False

    return SameUserOrReadOnly
