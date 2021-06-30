from unittest import mock

from .testcases import UserAuthenticatedTestCase
from ..exceptions import InvalidCredentials, JSONWebTokenExpired
from ..middleware import TokenAuthenticationMiddleware


class JWTMiddlewareTest(UserAuthenticatedTestCase):

    def setUp(self):
        super(JWTMiddlewareTest, self).setUp()
        self.middleware = TokenAuthenticationMiddleware()

    def test_authenticate_request(self):
        info = self.get_authenticated_info_context()
        next_middleware = mock.Mock()

        self.middleware.resolve(next_middleware, None, info)
        self.assertEqual(info.context.user, self.user)
        next_middleware.assert_called_once_with(None, info)

    def test_invalid_tokens(self):
        info = self.get_authenticated_info_context(access_token='INVALID_ACCESS_TOKEN',
                                                   refresh_token='INVALID_REFRESH_TOKEN')
        next_middleware = mock.Mock()

        with self.assertRaises(InvalidCredentials):
            self.middleware.resolve(next_middleware, None, info)

        next_middleware.assert_not_called()

    def test_revoked_token(self):
        info = self.get_authenticated_info_context()
        next_middleware = mock.Mock()
        with self.assertRaises(JSONWebTokenExpired):
            self.refresh_token_instance.revoke()
            self.middleware.resolve(next_middleware, None, info)

        next_middleware.assert_not_called()
