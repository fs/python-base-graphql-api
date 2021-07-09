from django.utils.translation import gettext_lazy as _


class JSONWebTokenError(Exception):
    """Raises in JWT authentication module."""

    default_message = None

    def __init__(self, message=None):
        """Added default message for errors."""
        if message is None:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(JSONWebTokenError):
    """Raises with expired tokens."""

    default_message = _('You do not have permission to perform this action')


class InvalidCredentials(JSONWebTokenError):
    """Raises for invalid username:password."""

    default_message = _('Invalid credentials')


class ResetTokenExpired(Exception):
    """Raise in password recovery by reset token."""

    def __init__(self, message=None):
        """Added default message."""
        if message is None:
            message = _('Reset token expired')

        super().__init__(message)
