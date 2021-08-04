from typing import Dict, List, NoReturn, Optional, Union

from django.contrib.auth import get_user_model
from graphene.types import Context
from server.apps.users.models import ResetToken
from server.apps.users.tasks import send_recovery_email
from server.core.auth.jwt.exceptions import (
    InvalidCredentials,
    ResetTokenInvalid,
)

User = get_user_model()


class UpdateUserMixin:
    """Mixin for user fields update."""

    @staticmethod
    def change_password(user: User, current_password: str, password: str) -> NoReturn:
        """Check and set password for user."""
        password_is_true = user.check_password(current_password)

        if not password_is_true:
            raise InvalidCredentials()

        user.set_password(password)

    @staticmethod
    def update_avatar(user: User, avatar: Dict[str, Union[str, Dict]]) -> NoReturn:
        """Saving user avatar url from AWS."""
        user.avatar.save(avatar.get('id'), content=None)

    @staticmethod
    def update_user_fields(user: User, upd_fields: Dict[str, str]):
        """Set updated values for user model."""
        for field_name, field_val in upd_fields.items():
            setattr(user, field_name, field_val)

        user.save()

    @classmethod
    def update_user(cls, request: Context, input_: Dict[str, Union[str, Dict]]) -> NoReturn:
        """Update user fields."""
        user = request.user
        current_password = input_.pop('current_password')
        password = input_.pop('password')
        avatar = input_.pop('avatar')

        if avatar:
            cls.update_avatar(user, avatar)

        if current_password and password:
            cls.change_password(user, current_password, password)

        cls.update_user_fields(user, input_)


class ImagePresignMixin:
    """Mixin for image direct uploading."""

    @classmethod
    def get_presign_upload(cls, user: User, filename: str, file_type: str) -> List[Dict[str, str]]:
        """Generate url and headers for AWS direct upload from frontend."""
        return user.avatar.storage.generate_presigned_post(filename, file_type)


class PasswordRecoveryMixin:
    """Mixin for user password recovery request."""

    @classmethod
    def recovery(cls, email: str) -> Optional[User]:
        """Create reset token and send password recovery email."""
        user = User.objects.filter(email=email)

        if user.exists():
            reset_token = ResetToken.objects.create(user=user[0])
            send_recovery_email.delay(reset_token_pk=reset_token.pk)
            return reset_token
        return None


class UpdatePasswordMixin:
    """Updating password by received email with reset token."""

    @classmethod
    def update_password(cls, password: str, reset_token: str) -> User:
        """Setting new password for user by reset token."""
        try:
            reset_token = ResetToken.objects.get_active_token(token=reset_token)
        except ResetToken.DoesNotExist:
            raise ResetTokenInvalid()

        reset_token.set_password(password)
        return reset_token.user
