from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from ..serializers import (
    UserSerializer,
)
from .permissions import AnonUserPost, same_user


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all().order_by("id")
    permission_classes = [same_user(), AnonUserPost]

    def get_serializer_class(self):
        return UserSerializer
