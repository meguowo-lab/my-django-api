from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as PwdValidationError
from rest_framework.validators import ValidationError

from .base import BaseSerializer

user_model = get_user_model()


class UserSerializer(BaseSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if instance != self.context["request"].user:
            rep.pop("email")

        return rep

    def update(self, instance, validated_data):
        if instance.email != validated_data["email"]:
            instance.email_verified = False
        return super().update(instance, validated_data)

    def validate(self, attrs):
        if "password" in attrs.keys():
            user = user_model(**attrs)

            try:
                validate_password(attrs["password"], user)
            except PwdValidationError as e:
                raise ValidationError({"errors": e.messages})

        return super().validate(attrs)

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].method != "POST":
            fields.pop("password")

        return fields

    class Meta:
        model = user_model
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
