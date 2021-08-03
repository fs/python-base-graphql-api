from datetime import timedelta
from unittest import mock

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from server.core.authentication.jwt import mixins
from server.core.authentication.jwt.exceptions import PermissionDenied
from server.core.authentication.jwt.middleware import TokenAuthenticationMiddleware
from server.core.authentication.jwt.models import RefreshToken
from tests.test_server.test_jwt.testcases import UserAuthenticatedTestCase
from server.core.authentication.jwt.utils import jwt_decode


class MiddlewareSetupMixin:
    """Mixin for middleware setup."""

    def setUp(self):
        """Setup authentication middleware resolver."""
        super().setUp()
        self.middleware_resolver = TokenAuthenticationMiddleware().resolve


class ObtainPairMixinTest(UserAuthenticatedTestCase):
    """Obtain pair mixin test. Uses with mutation."""

    def test_generate_pair(self):
        """Test generate tokens pair by user."""
        tokens = self.generate_pair(self.user)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']

        access_payload = jwt_decode(access_token)

        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)
        self.assertTrue(RefreshToken.objects.filter(token=refresh_token).exists())
        self.assertTrue(RefreshToken.objects.access_token_is_active(access_payload['jti']))

    def test_generate_pair_with_anonymous(self):
        """Test generate tokens pair by anonymous."""
        anonymous_user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            self.generate_pair(anonymous_user)


class RevokeTokenMixinTest(mixins.RevokeTokenMixin, MiddlewareSetupMixin, UserAuthenticatedTestCase):
    """Test token revoking by mocked request."""

    def test_revoke_single_token(self):
        """Test token revoking in authenticated in current session."""
        authenticated_info = self.get_authenticated_info_context()
        everywhere = False
        self.generate_refresh_tokens()
        self.logout(request=authenticated_info.context, everywhere=everywhere)
        self.assertFalse(self.refresh_token_instance.is_active)
        self.assertTrue(RefreshToken.objects.get_active_tokens_for_sub(self.user.pk).exists())

    def generate_refresh_tokens(self):
        """Generate refresh tokens with different creation time."""
        now = timezone.now()
        created_at_times = [now + timedelta(hours=index) for index in range(1, 5)]

        for created_at in created_at_times:
            RefreshToken.objects.create(user=self.user, created_at=created_at)

    def test_revoke_all_user_tokens(self):
        """Test token revoking in all user sessions."""
        authenticated_info = self.get_authenticated_info_context()
        everywhere = True
        self.generate_refresh_tokens()

        self.logout(request=authenticated_info.context, everywhere=everywhere)
        self.assertFalse(RefreshToken.objects.get_active_tokens_for_sub(self.user.pk).exists())

    def test_revoke_session(self):
        """Test session revoking."""
        authenticated_info = self.get_authenticated_info_context()
        context = authenticated_info.context
        self.logout(request=context)
        next_middleware = mock.Mock()
        self.middleware_resolver(next_middleware, None, authenticated_info)

        self.assertFalse(context.user.is_authenticated)
        self.assertEqual(context.refresh_token, None)


class UpdateTokenPairMixinTest(mixins.UpdateTokenPairMixin, MiddlewareSetupMixin, UserAuthenticatedTestCase):
    """Test token pair updating by authenticated request."""

    def test_non_authenticated_request(self):
        """Test update pair with non authenticated request."""
        request = self.info().context
        request.user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            self.update_pair(request)
