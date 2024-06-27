from ..models import News
from .base import BaseSerializer
from .user import UserSerializer


class NewsSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        self.attach_user(validated_data)
        return super().create(validated_data)

    class Meta:
        model = News
        fields = ["id", "user", "title", "body", "created_at", "image"]
