from ..models import Comment
from .user import UserSerializer
from .with_user import WithUserSerializer


class CommentSerializer(WithUserSerializer):
    user = UserSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].method in ["UPDATE", "PUT"]:
            fields.pop("news_id")
        return fields

    class Meta:
        model = Comment
        fields = ["id", "user", "news_id", "created_at", "body"]
