from datetime import datetime
from calendar import timegm

from .models import RefreshToken
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import jwt_decode, jwt_encode, jwt_payload
from .models import RefreshToken

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class GenerateTokenMixin:

    @staticmethod
    def _generate_access_token(user, now):
        exp = now + jwt_settings.get('ACCESS_TOKEN_EXPIRATION_DELTA')
        payload = jwt_payload(user, exp, 'access')
        return jwt_encode(payload)

    @staticmethod
    def _generate_refresh_token(user, now):
        return RefreshToken.objects.create(user=user, now=now)


class ObtainPairMixin(GenerateTokenMixin):

    @classmethod
    def generate_pair(cls, user):
        now = datetime.now()

        return {
            "access_token": cls._generate_access_token(user, now),
            "refresh_token": cls._generate_refresh_token(user, now).token
        }


class UpdateAccessTokenMixin(GenerateTokenMixin):

    @classmethod
    def update_pair(cls, request, user):
        pass



