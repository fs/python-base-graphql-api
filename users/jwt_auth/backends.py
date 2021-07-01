from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from jwt.exceptions import DecodeError

from .models import RefreshToken
from .exceptions import PermissionDenied
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
                raise PermissionDenied()

            try:
                user = User.objects.get(pk=payload.get('sub'))
                access_token_is_active = user.refresh_tokens.access_token_is_active(jti=payload['jti'])

                return user if access_token_is_active else None

            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        return None
