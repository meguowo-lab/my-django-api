from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..email import start_email_verify
from .permissions.email_unverified import EmailUnverifiedOrReadOnly


@api_view(["POST"])
@permission_classes([IsAuthenticated, EmailUnverifiedOrReadOnly])
def verify_email_view(req: Request):
    start_email_verify(req)
    return Response("please check your email")
