from .email_verified import EmailVerifiedOrReadOnly
from .or_read import or_read


class EmailUnverifiedOrReadOnly(EmailVerifiedOrReadOnly):
    @or_read
    def has_permission(self, request, view):
        return not request.user.email_verified
