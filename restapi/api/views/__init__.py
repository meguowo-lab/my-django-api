from rest_framework.routers import DefaultRouter

from . import permissions
from .comments import CommentViewSet
from .news import NewsViewSet
from .user import UserViewSet
from .verify_email import verify_email_view
from .verify_email_complete import verify_email_complete_view

router = DefaultRouter()
router.register("news", NewsViewSet)
router.register("comments", CommentViewSet)
router.register("users", UserViewSet)

__all__ = ["permissions", "router", "verify_email_complete_view", "verify_email_view"]
