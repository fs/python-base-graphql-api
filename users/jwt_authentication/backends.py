from django.contrib.auth import get_user_model
from .utils import get_access_token_by_request, get_user_by_access_token

User = get_user_model()


class JSONWebTokenBackend:

    def authenticate(self, request=None, **kwargs):
        if request is None or getattr(request, '_jwt_token_auth', False):
            return None

        access_token = get_access_token_by_request(request)

        if access_token is not None:
            return get_user_by_access_token(access_token)

        return None

    def get_user(self, user_id):
        return None
