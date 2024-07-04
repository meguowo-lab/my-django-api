from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer


class WithUserSerializer(ModelSerializer):
    def _attach_user(self, validated_data):
        user = CurrentUserDefault()(self)
        validated_data["user_id"] = user

    def create(self, validated_data):
        self._attach_user(validated_data)
        return super().create(validated_data)
