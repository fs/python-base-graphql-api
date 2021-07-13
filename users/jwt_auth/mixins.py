from django.conf import settings
from django.contrib.auth import get_user_model
from users.jwt_auth.exceptions import InvalidCredentials, ResetTokenExpired
from users.jwt_auth.models import RefreshToken, ResetToken
from users.jwt_auth.utils import jwt_encode

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class ObtainPairMixin:
    """Mixin for tokens pair generation by user."""

    @classmethod
    def generate_pair(cls, user):
        """Create tokens pair with same JTI."""
        refresh_token = RefreshToken.objects.create(user=user)
        access_payload = refresh_token.get_payload_by_token()
        access_payload['type'] = 'access'
        access_token = jwt_encode(access_payload)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token.token,
        }


class RevokeTokenMixin:
    """Mixin for user logout."""

    @classmethod
    def logout(cls, request, everywhere=False):
        """Revoking refresh tokens."""
        if not getattr(request, 'user', None):
            return None

        if everywhere:
            RefreshToken.objects.revoke_all_for_user(request.user)
        else:
            request.refresh_token.revoke()


class UpdateTokenPairMixin(ObtainPairMixin):
    """Mixin for updating tokens."""

    @classmethod
    def update_pair(cls, request):
        """Revoking and generation tokens."""
        request.refresh_token.revoke()
        return cls.generate_pair(request.user)


class UpdateUserMixin:
    """Mixin for user fields update."""

    @staticmethod
    def change_password(user, current_password, password):
        """Check and set password for user."""
        password_is_true = user.check_password(current_password)

        if not password_is_true:
            raise InvalidCredentials()

        user.set_password(password)

    @staticmethod
    def update_avatar(user, avatar):
        """Saving user avatar url from AWS."""
        user.avatar.save(avatar.get('id'), content=None)

    @staticmethod
    def update_user_fields(user, upd_fields):
        """Set updated values for user model."""
        for field_name, field_val in upd_fields.items():
            setattr(user, field_name, field_val)

        user.save()

    @classmethod
    def update_user(cls, request, input_):
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
    def get_presign_upload(cls, user, filename, file_type):
        """Generate url and headers for AWS direct upload from frontend."""
        return user.avatar.storage.generate_presigned_post(filename, file_type)


class PasswordRecoveryMixin:
    """Mixin for user password recovery request."""

    @classmethod
    def recovery(cls, email):
        """Create reset token and send password recovery email."""
        user = User.objects.filter(email=email)

        if user.exists():
            reset_token = ResetToken.objects.create(user=user[0])
            reset_token.send_recovery_mail()
            return user[0]
        return None


class UpdatePasswordMixin:
    """Updating password by received email with reset token."""

    @classmethod
    def update_password(cls, password, reset_token):
        """Setting new password for user by reset token."""
        reset_token = ResetToken.objects.get(token=reset_token)
        if not reset_token.is_active:
            raise ResetTokenExpired()

        reset_token.set_password(password)
        return reset_token.user
