from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from jwt.exceptions import DecodeError

from .models import RefreshToken
from .utils import get_refresh_token_by_request, get_access_token_by_request, jwt_decode
from .exceptions import InvalidCredentials

jwt_settings = settings.JWT_SETTINGS


class TokenAuthenticationMiddleware:

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        user = authenticate(context)
        context.user = user or AnonymousUser()

        return next(root, info, **kwargs)
