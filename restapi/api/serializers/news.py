from ..models import News
from .user import UserSerializer
from .with_user import WithUserSerializer


class NewsSerializer(WithUserSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = News
        fields = ["id", "user", "title", "body", "created_at", "image"]
