from django.contrib.auth import get_user_model
from .utils import get_access_token_by_request, get_user_by_access_token, jwt_decode
from .models import RefreshToken

User = get_user_model()


class JSONWebTokenBackend:

    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        access_token = get_access_token_by_request(request)

        if access_token is not None:
            payload = jwt_decode(access_token)

            related_refresh_token = RefreshToken.objects\
                .get_active_tokens_for_user(payload.get('sub'))\
                .filter(jti=payload.get('jti'))

            if related_refresh_token.exists():
                return related_refresh_token[0].user

        return None

    def get_user(self, user_id):
        return None
