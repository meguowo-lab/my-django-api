from rest_framework.permissions import SAFE_METHODS


def or_read(func):
    def wrapper(*args, **kwargs):
        if args[1].method in SAFE_METHODS:
            return True

        res = func(*args, **kwargs)
        return res

    return wrapper
