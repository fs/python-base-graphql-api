from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import jwt_encode
from .models import RefreshToken, ResetToken
from .exceptions import InvalidCredentials

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class ObtainPairMixin:

    @classmethod
    def generate_pair(cls, user):
        refresh_token = RefreshToken.objects.create(user=user)
        access_payload = refresh_token.get_payload_by_token()
        access_payload['type'] = 'access'
        access_token = jwt_encode(access_payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token.token,
        }


class RevokeTokenMixin:

    @classmethod
    def logout(cls, request, everywhere=False):
        if not hasattr(request, 'user') or not hasattr(request, 'refresh_token'):
            return None

        if everywhere:
            RefreshToken.objects.revoke_all_for_user(request.user)
        else:
            request.refresh_token.revoke()


class UpdateTokenPairMixin(ObtainPairMixin):

    @classmethod
    def update_pair(cls, request):
        request.refresh_token.revoke()
        return cls.generate_pair(request.user)


class UpdateUserMixin:

    @staticmethod
    def change_password(user, current_password, password):
        password_is_true = user.check_password(current_password)

        if not password_is_true:
            raise InvalidCredentials()

        user.set_password(password)

    @staticmethod
    def update_avatar(user, avatar):
        user.avatar.save(avatar.get("id"), content=None)

    @classmethod
    def update_user(cls, request, input):
        user = request.user
        current_password = input.pop('current_password')
        password = input.pop('password')
        avatar = input.pop('avatar')

        if avatar:
            cls.update_avatar(user, avatar)

        if current_password and password:
            cls.change_password(user, current_password, password)

        for key in input:
            setattr(user, key, input[key])

        user.save()


class ImagePresignMixin:

    @classmethod
    def get_presign_upload(cls, user, filename, file_type):
        return user.avatar.storage.generate_presigned_post(filename, file_type)


class PasswordRecoveryMixin:

    @classmethod
    def recovery(cls, email):
        user = User.objects.filter(email=email)

        if user.exists():
            reset_token = ResetToken.objects.create(user=user[0])
            reset_token.send_recovery_mail()


class UpdatePasswordMixin:

    @classmethod
    def update_password(cls, password, reset_token):
        reset_token = ResetToken.objects.get(token=reset_token)
        if not reset_token.is_active:
            raise Exception("Reset token already used")

        reset_token.set_password(password)
        return reset_token.user
