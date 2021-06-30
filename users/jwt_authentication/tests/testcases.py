from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from graphql.execution.execute import GraphQLResolveInfo

from ..mixins import ObtainPairMixin
from ..models import RefreshToken

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class UserAuthenticatedTestCase(ObtainPairMixin, TestCase):

    def setUp(self):
        user = User.objects.create(email='test@test.test')
        user.set_password('test')
        tokens = self.generate_pair(user)

        self.user = user
        self.access_token = tokens.get('access_token')
        self.refresh_token = tokens.get('refresh_token')
        self.refresh_token_instance = RefreshToken.objects.get(token=self.refresh_token)
        self.request_factory = RequestFactory()

    def info(self, user=None, headers={}, cookies={}):
        request = self.request_factory.post('/', **headers)
        request.COOKIES = cookies

        if user:
            request.user = user

        return mock.Mock(
            context=request,
            path=['test'],
            spec=GraphQLResolveInfo,
        )

    def get_authenticated_info_context(self, access_token=None, refresh_token=None):
        access_token_header = jwt_settings.get('JWT_AUTH_HEADER_NAME')
        access_token_prefix = jwt_settings.get('JWT_AUTH_HEADER_PREFIX')
        refresh_token_cookie_name = jwt_settings.get('JWT_REFRESH_TOKEN_COOKIE_NAME')

        headers = {
            access_token_header: f'{access_token_prefix} {access_token or self.access_token}',
        }

        cookies = {
            refresh_token_cookie_name: refresh_token or self.refresh_token
        }

        return self.info(user=None, headers=headers, cookies=cookies)
