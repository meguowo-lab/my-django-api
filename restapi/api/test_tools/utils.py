from typing import Any, Callable

from django.contrib.auth import get_user_model


def create_superuser(password: str):
    user_model = get_user_model()
    return user_model.objects.create_superuser(
        username="test_rit", email="testmail@testmail.com", password=password
    )


def performing(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any):
        serializer_cls_name = type(args[0]).__name__
        print(f"{serializer_cls_name} performing {func.__name__}...")
        func(*args, **kwargs)
        print(f"{serializer_cls_name} succesfully performed {func.__name__}!")

    return wrapper
