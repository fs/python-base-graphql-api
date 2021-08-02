from unittest import mock

from django.contrib.auth.models import AnonymousUser
from server.core.authentication.jwt.exceptions import PermissionDenied
from server.core.authentication.jwt.middleware import TokenAuthenticationMiddleware
from tests.test_server.test_jwt.testcases import UserAuthenticatedTestCase


class JWTMiddlewareTest(UserAuthenticatedTestCase):
    """Testing authentication middleware."""

    def setUp(self):
        """Setup middleware."""
        super().setUp()
        self.middleware = TokenAuthenticationMiddleware()

    def test_authenticate_request(self):
        """Test authenticated context."""
        info = self.get_authenticated_info_context()
        context = info.context
        next_middleware = mock.Mock()

        self.middleware.resolve(next_middleware, None, info)
        self.assertEqual(context.user, self.user)
        self.assertEqual(context.refresh_token, self.refresh_token_instance)

        next_middleware.assert_called_once_with(None, info)

    def test_invalid_tokens(self):
        """Test context with invalid tokens."""
        info = self.get_authenticated_info_context(
            access_token='INVALID_ACCESS_TOKEN',
            refresh_token='INVALID_REFRESH_TOKEN',
        )
        context = info.context
        next_middleware = mock.Mock()
        self.middleware.resolve(next_middleware, None, info)

        with self.assertRaises(PermissionDenied):
            # context.user and context.refresh_token wraps in django.utils.functional.SimpleLazyObject
            self.assertEqual(context.user, AnonymousUser())

        # assertIsNone don`t work with SimpleLazyObject
        self.assertEqual(context.refresh_token, None)
        next_middleware.assert_called_once_with(None, info)

    def test_revoked_token(self):
        """Test context with valid tokens, but revoked refresh token."""
        info = self.get_authenticated_info_context()
        context = info.context

        next_middleware = mock.Mock()
        self.refresh_token_instance.revoke()
        self.middleware.resolve(next_middleware, None, info)

        self.assertEqual(context.user, AnonymousUser())
        self.assertEqual(context.refresh_token, None)
        next_middleware.assert_called_once_with(None, info)
