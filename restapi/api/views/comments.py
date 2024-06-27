from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.viewsets import ModelViewSet

from ..models import Comment
from ..serializers import (
    CommentSerializer,
)
from .permissions import EmailVerifiedOrReadOnly, same_user


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by("id")
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        same_user("user"),
        EmailVerifiedOrReadOnly,
    ]
    filterset_fields = ["user", "news", "id", "body", "created_at"]
    filter_backends = [DjangoFilterBackend]
