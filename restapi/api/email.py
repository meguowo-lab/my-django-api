from threading import Thread

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse


def create_verify_url(req: HttpRequest, user_id: int, token: str):
    return req.build_absolute_uri(
        reverse("email_verify", kwargs={"pk": user_id, "token": token}),
    )


def send_email(subject: str, body: str, to: list[str], content_subtype: str = "text"):
    e = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
    )

    e.content_subtype = content_subtype

    th = Thread(target=e.send)

    th.start()


def send_verifier_email(req: HttpRequest, token: str):
    user = req.user
    send_email(
        subject="email verify",
        body=render_to_string(
            "email_msg.html",
            {"verify_url": create_verify_url(req, user.id, token), "user": user},
        ),
        to=[user.email],
        content_subtype="html",
    )


def start_email_verify(
    req: HttpRequest, gen: PasswordResetTokenGenerator = default_token_generator,
):
    """Starts email verification process and saves user"""
    token = gen.make_token(req.user)

    send_verifier_email(req, token)


def verify_token(
    user, token: str, gen: PasswordResetTokenGenerator = default_token_generator,
):
    verified = gen.check_token(user, token)

    return verified


def complete_email_verify(user_id: int, token: str):
    user_model = get_user_model()
    user = user_model.objects.get(id=user_id)

    verified = verify_token(user, token)

    if verified:
        user.email_verified = True
        user.save()

    return verified
