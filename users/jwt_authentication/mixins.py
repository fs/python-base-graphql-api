from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import jwt_encode
from .models import RefreshToken
from .exceptions import InvalidCredentials
from django.forms.models import model_to_dict

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
        user_fields = list(input.keys()) + ['id', 'avatar']
        return model_to_dict(user, user_fields)


class ImagePresignMixin:

    @classmethod
    def get_presign_upload(cls, user, filename, file_type):
        return user.avatar.storage.generate_presigned_post(filename, file_type)






