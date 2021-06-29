from unittest import mock

from django.contrib.auth.models import AnonymousUser

from .testcases import UserAuthenticatedTestCase
from ..middleware import TokenAuthenticationMiddleware
from ..exceptions import InvalidCredentials
from ..utils import jwt_encode, jwt_decode


class JWTMiddlewareTest(UserAuthenticatedTestCase):

    def setUp(self):
        super(JWTMiddlewareTest, self).setUp()
        self.middleware = TokenAuthenticationMiddleware()

    def test_next_middleware_call(self):
        next_middleware = mock.Mock()
        info = self.get_authenticated_info_context()
        self.middleware.resolve(next_middleware, None, info)
        next_middleware.assert_called_once_with(None, info)

    def test_authenticate_request(self):
        info = self.get_authenticated_info_context()
        next_middleware = mock.Mock()

        self.middleware.resolve(next_middleware, None, info)

        self.assertEqual(info.context.user, self.user)
        self.assertEqual(info.context.refresh_token.token, self.refresh_token)

    def test_invalid_tokens(self):
        info = self.get_authenticated_info_context(access_token='INVALID_ACCESS_TOKEN',
                                                   refresh_token='INVALID_REFRESH_TOKEN')
        next_middleware = mock.Mock()

        self.middleware.resolve(next_middleware, None, info)
        self.assertEqual(info.context.user, AnonymousUser())
        self.assertEqual(info.context.refresh_token, None)

    def test_different_token_users(self):
        payload = jwt_decode(self.refresh_token)
        payload['sub'] = 2
        payload['type'] = 'access'
        access_token = jwt_encode(payload)
        info = self.get_authenticated_info_context(access_token=access_token)
        next_middleware = mock.Mock()

        with self.assertRaises(InvalidCredentials):
            self.middleware.resolve(next_middleware, None, info)

        self.assertEqual(info.context.user, AnonymousUser())
        self.assertEqual(info.context.refresh_token, None)







