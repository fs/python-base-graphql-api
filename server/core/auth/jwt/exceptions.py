from django.utils.translation import gettext_lazy as _


class BaseError(Exception):
    """Base abstract exception."""

    default_message = None

    def __init__(self, message=None):
        """Added default message for errors."""
        if message is None:
            message = self.default_message

        super().__init__(message)


class JSONWebTokenError(BaseError):
    """Raises in JWT auth module."""


class PermissionDenied(JSONWebTokenError):
    """Raises with expired tokens."""

    default_message = _('You do not have permission to perform this action')


class InvalidCredentials(JSONWebTokenError):
    """Raises for invalid username:password."""

    default_message = _('Invalid credentials')


class ResetTokenException(BaseError):
    """Exception for reset token errors."""


class ResetTokenInvalid(ResetTokenException):
    """Raise in password recovery process."""

    default_message = _('Reset token is invalid or expired')
