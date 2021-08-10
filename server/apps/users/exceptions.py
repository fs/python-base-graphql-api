class UserProfileException(Exception):
    """Exceptions for user actions."""

    default_message = None

    def __init__(self, message=None):
        """Added default message for errors."""
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserAlreadyJoined(UserProfileException):
    """Raises when user already joined with that username."""

    default_message = 'User already joined'


class ValidationError(UserProfileException):
    """Validation error for fields."""

    default_message = 'Validation error'
