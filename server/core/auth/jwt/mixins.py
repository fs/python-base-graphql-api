from typing import Dict, NoReturn, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from graphene.types import Context
from server.core.auth.jwt.exceptions import PermissionDenied
from server.core.auth.jwt.models import RefreshToken
from server.core.auth.jwt.utils import jwt_encode

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class ObtainPairMixin:
    """Mixin for tokens pair generation by user."""

    @classmethod
    def generate_pair(cls, user: User, parent_token: Optional[RefreshToken] = None) -> Dict[str, str]:
        """Create tokens pair with same JTI."""
        if not isinstance(user, User):
            raise PermissionDenied()

        token_kwargs = cls.generate_token_kwargs(user, parent_token)
        refresh_token = RefreshToken.objects.create(**token_kwargs)
        return cls.get_tokens_pair(refresh_token)

    @classmethod
    def generate_access_token(cls, refresh_token: RefreshToken) -> str:
        """Generate access token by refresh token payload."""
        access_payload = refresh_token.get_payload_by_token()
        access_payload['type'] = 'access'
        return jwt_encode(access_payload)

    @classmethod
    def generate_token_kwargs(cls, user: User, parent_token: Optional[RefreshToken] = None) -> Dict:
        """Generate new token kwargs."""
        token_kwargs = {'user': user}
        if parent_token:
            token_kwargs.update({'parent_token': parent_token})
            parent_token.prolong_grace_period()

        return token_kwargs

    @classmethod
    def get_tokens_pair(cls, refresh_token: RefreshToken) -> Dict[str, str]:
        """Generate token pairs by refresh token."""
        access_token = cls.generate_access_token(refresh_token)
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

        refresh_token = request.refresh_token

        if not refresh_token.is_active:
            raise PermissionDenied()

        if substitution_token := getattr(refresh_token, 'substitution_token', False):  # noqa:WPS332
            return cls.get_tokens_pair(substitution_token)

        return cls.generate_pair(request.user, refresh_token)
