from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django.utils.translation import gettext_lazy


class UserManager(_UserManager):
    def create_superuser(
        self, username: str, email: str, password: str | None, **extra_fields: Any
    ) -> Any:
        extra_fields["email_verified"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(gettext_lazy("email address"), blank=False, unique=True)
    email_verified = models.BooleanField(default=False, null=False)
    objects = UserManager()


class News(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/images", null=True, blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Comment(models.Model):
    user_id = models.ForeignKey(User, models.CASCADE)
    news_id = models.ForeignKey(
        News,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="comments",
    )
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
