from django.contrib.auth.models import AnonymousUser
from users.jwt_auth import mixins
from users.jwt_auth.exceptions import PermissionDenied
from users.jwt_auth.models import RefreshToken
from users.jwt_auth.tests.testcases import UserAuthenticatedTestCase
from users.jwt_auth.utils import jwt_decode


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


class RevokeTokenMixinTest(mixins.RevokeTokenMixin, UserAuthenticatedTestCase):
    """Token revoking mixin. """

    def test_revoke_token(self):
        pass
