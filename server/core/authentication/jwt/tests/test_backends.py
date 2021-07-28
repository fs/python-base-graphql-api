from django.conf import settings
from users.jwt_auth import backends
from users.jwt_auth.exceptions import PermissionDenied
from users.jwt_auth.tests.testcases import UserAuthenticatedTestCase

jwt_settings = settings.JWT_SETTINGS


def get_auth_headers(access_token):
    """Making authentication headers for request."""
    access_token_header = jwt_settings.get('JWT_AUTH_HEADER_NAME')
    access_token_prefix = jwt_settings.get('JWT_AUTH_HEADER_PREFIX')
    return {
        access_token_header: f'{access_token_prefix} {access_token}',
    }


class BackendTest(UserAuthenticatedTestCase):
    """Backend authentication test cases."""

    def setUp(self):
        """Setup backend."""
        super().setUp()
        self.backend = backends.JSONWebTokenBackend()

    def test_authenticate(self):
        """Test authenticate with true credentials."""
        headers = get_auth_headers(self.access_token)
        request = self.info(headers=headers).context
        user = self.backend.authenticate(request)
        self.assertEqual(user, self.user)

    def test_revoked_refresh_token(self):
        """Test authenticate when all refresh tokens are revoked."""
        info = self.get_authenticated_info_context()
        self.user.refresh_tokens.revoke_all_for_user(self.user)
        user = self.backend.authenticate(info.context)
        self.assertIsNone(user)

    def test_authenticate_invalid(self):
        """Test invalid access token authentication."""
        request = self.get_authenticated_info_context(access_token='INVALID_ACCESS_TOKEN').context
        with self.assertRaises(PermissionDenied):
            self.backend.authenticate(request)

    def test_authenticate_null_request(self):
        """Test null request authenticate."""
        user = self.backend.authenticate(request=None)
        self.assertIsNone(user)

    def test_get_user(self):
        """Test get user, must return None."""
        user = self.backend.get_user(self.user.pk)
        self.assertIsNone(user)
