from threading import Event, Thread
from typing import NamedTuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

email_sent_event = Event()


class EmailTemplate(NamedTuple):
    template: str
    type: str


class EmailResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        token = super()._make_hash_value(user, timestamp)
        return f"{token}{user.email_verified}"


token_generator = EmailResetTokenGenerator()


def create_verify_url(req: HttpRequest, user_id: int, token: str):
    return req.build_absolute_uri(
        reverse("email_verify", kwargs={"pk": user_id, "token": token}),
    )


def thread_send_email(e: EmailMessage):
    email_sent_event.clear()
    e.send()
    email_sent_event.set()


def send_email(subject: str, body: str, to: list[str], content_subtype: str = "text"):
    e = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
    )

    e.content_subtype = content_subtype

    th = Thread(target=thread_send_email, args=[e])

    th.start()


def get_email_template(verify_url: str, user):
    template: str = settings.EMAIL_TEMPLATE
    if template.endswith(".html"):
        rendered_template = render_to_string(
            template,
            {"verify_url": verify_url, "user": user},
        )
        return EmailTemplate(template=rendered_template, type="html")

    return EmailTemplate(template=f"{template}{verify_url}", type="text")


def send_verifier_email(req: HttpRequest, token: str):
    user = req.user
    template, content_type = get_email_template(
        create_verify_url(req, user.id, token), user
    )
    send_email(
        subject="email verify",
        body=template,
        to=[user.email],
        content_subtype=content_type,
    )


def start_email_verify(
    req: HttpRequest,
    gen: EmailResetTokenGenerator = token_generator,
):
    """Starts email verification process and saves user"""
    token = gen.make_token(req.user)

    send_verifier_email(req, token)


def verify_token(
    user,
    token: str,
    gen: EmailResetTokenGenerator = token_generator,
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
