from unittest import mock
from abc import ABC

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from graphql.execution.execute import GraphQLResolveInfo
from users.jwt_auth.mixins import ObtainPairMixin
from users.jwt_auth.models import RefreshToken

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class UserAuthenticatedTestCase(ABC, ObtainPairMixin, TestCase):
    """Abstract TestCase with credentials for authenticate."""

    def setUp(self):
        """Setup credentials."""
        user = User.objects.create(email='test@test.test')
        user.set_password('test')
        tokens = self.generate_pair(user)

        self.user = user
        self.access_token = tokens.get('access_token')
        self.refresh_token = tokens.get('refresh_token')
        self.refresh_token_instance = RefreshToken.objects.get(token=self.refresh_token)
        self.request_factory = RequestFactory()

    def info(self, user=None, headers=None, cookies=None):
        """Make graphene info mock with specified params."""
        request = self.request_factory.post('/', **(headers or {}))
        request.COOKIES = cookies or {}

        if user:
            request.user = user

        return mock.Mock(
            context=request,
            path=['test'],
            spec=GraphQLResolveInfo,
        )

    def get_authenticated_info_context(self, access_token=None, refresh_token=None):
        """Make graphene info with authenticated context."""
        access_token_header = jwt_settings.get('JWT_AUTH_HEADER_NAME')
        refresh_token_cookie_name = jwt_settings.get('JWT_REFRESH_TOKEN_COOKIE_NAME')

        headers = {
            access_token_header: '{prefix} {token}'.format(
                prefix=jwt_settings.get('JWT_AUTH_HEADER_PREFIX'),
                token=access_token or self.access_token,
            ),
        }

        cookies = {refresh_token_cookie_name: refresh_token or self.refresh_token}

        return self.info(user=None, headers=headers, cookies=cookies)
