from graphql_jwt.refresh_token.models import AbstractRefreshToken
from graphql_jwt.refresh_token.managers import RefreshTokenQuerySet as RefreshTokenQS
from graphql_jwt.utils import jwt_encode, jwt_decode
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from django.db import models
from django.conf import settings

from .utils import get_refresh_token_payload

# class RefreshTokenQuerySet(RefreshTokenQS):
#     def create(self, user, **kwargs):
#         pass


class RefreshToken(AbstractRefreshToken):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jwt_refresh_tokens',
        verbose_name=_('user'),
    )

    # objects = RefreshTokenQuerySet()

    def generate_token(self):
        now = datetime.now()
        self.created = now
        payload = get_refresh_token_payload(now)
        token = jwt_encode(payload)
        return token
    #
    # def get_token(self):
    #     if hasattr(self, '_cached_token'):
    #         return self._cached_token
    #
    #     return self.token


