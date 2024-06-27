from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import bad_request
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..email import complete_email_verify
from .permissions import EmailUnverifiedOrReadOnly, same_user


@api_view(["POST"])
@permission_classes([same_user(), IsAuthenticated, EmailUnverifiedOrReadOnly])
def verify_email_complete_view(req: Request, pk: int, token: str):
    verified = complete_email_verify(pk, token)
    if verified:
        return Response("email succesfully verified!")

    return bad_request(req, "Cannot verify given token, please try again!")
