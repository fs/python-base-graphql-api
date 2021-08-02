import time
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from server.core.authentication.jwt.models import RefreshToken, ResetToken
from tests.test_server.test_jwt.testcases import UserAuthenticatedTestCase

jwt_settings = settings.JWT_SETTINGS


class RefreshTokenTest(UserAuthenticatedTestCase):
    """Test RefreshToken model methods tests."""

    def setUp(self):
        """Setup model."""
        super().setUp()
        self.model = RefreshToken

    def test_str(self):
        """Test str() of model instance. That must be equal token in string."""
        self.assertEqual(str(self.refresh_token_instance), self.refresh_token)

    def test_is_expired(self):
        """Test is_expired property of instance."""
        refresh_token = self.refresh_token_instance
        refresh_token.created_at = timezone.now()
        refresh_token.save()

        self.assertTrue(refresh_token.is_expired)
        self.assertFalse(refresh_token.is_active)

    def test_save(self):
        """Test jti, created_at and token fields generation in save time."""
        time.sleep(1)  # needed for timezone.now() difference
        refresh_token = self.model.objects.create(user=self.user)
        self.assertIsNotNone(refresh_token.jti)
        self.assertIsNotNone(refresh_token.created_at)
        self.assertIsNotNone(refresh_token.token)

    def test_revoke(self):
        """Test revoke method."""
        refresh_token = self.refresh_token_instance
        self.assertIsNone(refresh_token.revoked_at)
        refresh_token.revoke()
        self.assertIsNotNone(refresh_token.revoked_at)
        self.assertFalse(refresh_token.is_active)

    def test_expires_at(self):
        """Test expires_at property of instance."""
        refresh_token = self.refresh_token_instance
        exp_delta = jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        expires_at = refresh_token.created_at + exp_delta

        self.assertEqual(refresh_token.expires_at, expires_at)

    def test_get_payload_by_token(self):
        """Test token decoding."""
        refresh_token = self.refresh_token_instance
        payload = refresh_token.get_payload_by_token()

        self.assertIsNotNone(payload)
        payload_params = ['exp', 'sub', 'jti', 'type']

        for key in payload_params:
            self.assertIn(key, payload)
            self.assertIsNotNone(payload[key])

        self.assertEqual(payload['type'], 'refresh')


class ResetTokenTest(UserAuthenticatedTestCase):
    """Test ResetToken model."""

    def setUp(self):
        """Setup model and instance of model."""
        super().setUp()
        self.model = ResetToken
        self.instance = ResetToken.objects.create(user=self.user)

    def test_str(self):
        """Test str() of model instance. That must be equal token in string."""
        self.assertEqual(str(self.instance), self.instance.token)

    def test_save(self):
        """Test token, created_at generation in saving time."""
        reset_token = self.model.objects.create(user=self.user)
        self.assertIsNotNone(reset_token.token)
        self.assertIsNotNone(reset_token.created_at)

    def test_set_password(self):
        """Test password setting for user by related reset token."""
        test_password = 'test_password_123'
        reset_token = self.model.objects.create(user=self.user)
        reset_token.set_password(test_password)

        self.assertTrue(self.user.check_password(test_password))
        self.assertTrue(reset_token.is_used)
        self.assertFalse(reset_token.is_active)

    def test_is_expired(self):
        """Test reset token expires."""
        settings.PASS_RESET_TOKEN_EXPIRATION_DELTA = timedelta(seconds=1)
        reset_token = self.model.objects.create(user=self.user)
        time.sleep(1)
        self.assertTrue(reset_token.is_expired)
