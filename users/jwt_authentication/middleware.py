from .utils import (get_user_by_access_token, get_access_token_by_request, get_refresh_token_by_request)
from django.conf import settings
from django.contrib.auth import login
from .models import RefreshToken

jwt_settings = settings.JWT_SETTINGS


class TokenAuthenticationMiddleware:

    @staticmethod
    def _authenticate(context, user, refresh_token):
        context.user = user
        context.refresh_token = refresh_token

    @staticmethod
    def get_refresh_token_instance(refresh_token):

        refresh_token_qs = RefreshToken.objects.filter(token=refresh_token)
        if refresh_token_qs.exists():
            return refresh_token_qs[0]

        return None

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        access_token = get_access_token_by_request(context)
        refresh_token = get_refresh_token_by_request(context)

        user = get_user_by_access_token(access_token)
        refresh_token_instance = self.get_refresh_token_instance(refresh_token)

        if user and refresh_token_instance:
            self._authenticate(context, access_token, refresh_token)

        return next(root, info, **kwargs)



