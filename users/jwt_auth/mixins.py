from typing import Dict, NoReturn, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from graphene.types import Context
from users.jwt_auth.exceptions import PermissionDenied
from users.jwt_auth.models import RefreshToken
from users.jwt_auth.utils import jwt_encode

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class ObtainPairMixin:
    """Mixin for tokens pair generation by user."""

    @classmethod
    def generate_pair(cls, user: User) -> Dict[str, str]:
        """Create tokens pair with same JTI."""
        if not isinstance(user, User):
            raise PermissionDenied()

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
    def logout(cls, request: Context, everywhere: Optional[bool] = False) -> NoReturn:
        """Revoking refresh tokens."""
        user = request.user
        if not isinstance(user, User):
            return None

        if everywhere:
            RefreshToken.objects.revoke_all_for_user(request.user)
        else:
            request.refresh_token.revoke()


class UpdateTokenPairMixin(ObtainPairMixin):
    """Mixin for updating tokens."""

    @classmethod
    def update_pair(cls, request: Context) -> Dict[str, str]:
        """Revoking and generation tokens."""
        if not request.user.is_authenticated:
            raise PermissionDenied()

        request.refresh_token.revoke()
        return cls.generate_pair(request.user)
