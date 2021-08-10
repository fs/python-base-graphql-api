from typing import Optional, Union

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from graphene.types import Context
from server.core.auth.jwt import utils
from server.core.auth.jwt.models import RefreshToken

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


def get_user(context: Context) -> Union[User, AnonymousUser, None]:
    """Needed for wrap in simple lazy object."""
    return getattr(context, '_cached_user', authenticate(context) or AnonymousUser())


def get_refresh_token_instance(context: Context) -> Optional[RefreshToken]:
    """Return refresh token instance by request."""
    access_payload = utils.get_access_payload_by_request(context)

    if not access_payload:
        return None

    try:
        return RefreshToken.objects.get_active_tokens_for_sub(access_payload['sub']).get(jti=access_payload['jti'])

    except RefreshToken.DoesNotExist:
        return None


def get_refresh_token(context: Context) -> Optional[RefreshToken]:
    """Needed for wrap in simple lazy object."""
    return getattr(context, '_cached_refresh_token', get_refresh_token_instance(context))


class TokenAuthenticationMiddleware:
    """JWT Authentication middleware for graphene."""

    def resolve(self, next, root, info, **kwargs):  # noqa: WPS125
        """Middleware resolver."""
        context = info.context
        access_token = utils.get_access_token_by_request(context)

        if access_token:
            context.user = SimpleLazyObject(lambda: get_user(context))
            context.refresh_token = SimpleLazyObject(lambda: get_refresh_token(context))

        return next(root, info, **kwargs)
