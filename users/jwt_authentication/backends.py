from django.contrib.auth import get_user_model
from jwt.exceptions import DecodeError

from .exceptions import JSONWebTokenExpired, InvalidCredentials
from .models import RefreshToken
from .utils import get_access_token_by_request, jwt_decode

User = get_user_model()


class JSONWebTokenBackend:

    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        access_token = get_access_token_by_request(request)

        if access_token is not None:

            try:
                payload = jwt_decode(access_token)
            except DecodeError:
                raise InvalidCredentials()

            related_active_refresh_token = RefreshToken.objects \
                .get_active_tokens_for_sub(payload.get('sub'), jti=payload.get('jti'))

            if related_active_refresh_token.exists():
                return related_active_refresh_token[0].user
            else:
                raise JSONWebTokenExpired()

        return None

    def get_user(self, user_id):
        return None
