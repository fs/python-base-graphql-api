from jwt.exceptions import DecodeError
from users import utils as users_utils
from users.jwt_auth import utils as jwt_utils
from users.jwt_auth.exceptions import PermissionDenied


class JSONWebTokenBackend:
    """JWT backend for authenticate user by access_token."""

    def authenticate(self, request=None, **kwargs):
        """Access token authentication logic."""
        if request is None:
            return None

        access_token = jwt_utils.get_access_token_by_request(request)

        if access_token is None:
            return None

        try:
            payload = jwt_utils.jwt_decode(access_token)

        except DecodeError:
            raise PermissionDenied()

        user = users_utils.utils.get_user_or_none(pk=payload.get('sub'))

        if not user:
            return None

        access_token_is_active = user.refresh_tokens.access_token_is_active(jti=payload['jti'])
        return user if access_token_is_active else None

    def get_user(self, user_id):
        """Used by django authentication system. We don`t need this method implementation."""
        return None  # noqa: WPS324
