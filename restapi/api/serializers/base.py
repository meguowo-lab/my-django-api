from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):
    def attach_user(self, validated_data):
        user = CurrentUserDefault()(self)
        validated_data["user"] = user
