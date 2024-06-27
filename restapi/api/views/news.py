from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.viewsets import ModelViewSet

from ..models import News
from ..serializers import (
    NewsSerializer,
)
from .permissions import same_user


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().order_by("id")
    serializer_class = NewsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, same_user("user")]
    filterset_fields = ["user", "id", "title", "body", "created_at"]
    filter_backends = [DjangoFilterBackend]
