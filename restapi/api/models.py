from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    email = models.EmailField(gettext_lazy("email address"), blank=False, unique=True)
    email_verified = models.BooleanField(default=False, null=False)


class News(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/images", null=True, blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    news = models.ForeignKey(
        News, models.CASCADE, null=False, blank=False, related_name="comments",
    )
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
