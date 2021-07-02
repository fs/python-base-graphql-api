from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from .models import RefreshToken
from .utils import get_access_payload_by_request, get_access_token_by_request

jwt_settings = settings.JWT_SETTINGS


def get_user(context):
    if not hasattr(context, '_cached_user'):
        context._cached_user = authenticate(context) or AnonymousUser()

    return getattr(context, '_cached_user')


def get_refresh_token(context):
    if not hasattr(context, '_cached_refresh_token'):
        access_payload = get_access_payload_by_request(context)
        context._cached_refresh_token = None

        if access_payload:
            try:
                context._cached_refresh_token = RefreshToken.objects \
                    .get_active_tokens_for_sub(access_payload['sub']) \
                    .get(jti=access_payload['jti'])

            except RefreshToken.DoesNotExist:
                pass

    return getattr(context, '_cached_refresh_token')


class TokenAuthenticationMiddleware:

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        access_token = get_access_token_by_request(context)

        if access_token:
            context.user = SimpleLazyObject(lambda: get_user(context))
            context.refresh_token = SimpleLazyObject(lambda: get_refresh_token(context))

        return next(root, info, **kwargs)
