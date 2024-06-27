from ..models import Comment
from .base import BaseSerializer
from .user import UserSerializer


class CommentSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        self.attach_user(validated_data)
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].method in ["UPDATE", "PUT"]:
            fields.pop("news")
        return fields

    class Meta:
        model = Comment
        fields = ["id", "user", "news", "created_at", "body"]
