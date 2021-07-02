from django.conf import settings
from django.utils import timezone

from .testcases import UserAuthenticatedTestCase
from ..models import RefreshToken, ResetToken

jwt_settings = settings.JWT_SETTINGS


class RefreshTokenTest(UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.model = RefreshToken

    def test_str(self):
        self.assertEqual(str(self.refresh_token_instance), self.refresh_token)

    def test_is_revoked(self):
        refresh_token = self.refresh_token_instance
        refresh_token.revoked_at = timezone.now()
        refresh_token.save()

        self.assertTrue(refresh_token.is_revoked)
        self.assertFalse(refresh_token.is_active)

    def test_is_expired(self):
        refresh_token = self.refresh_token_instance
        refresh_token.created_at = timezone.now()
        refresh_token.save()

        self.assertTrue(refresh_token.is_expired)
        self.assertFalse(refresh_token.is_active)

    def test_save(self):
        refresh_token = self.model.objects.create(user=self.user)

        self.assertIsNotNone(refresh_token.jti)
        self.assertIsNotNone(refresh_token.created_at)
        self.assertIsNotNone(refresh_token.token)

    def test_revoke(self):
        refresh_token = self.refresh_token_instance
        self.assertIsNone(refresh_token.revoked_at)
        refresh_token.revoke()
        self.assertIsNotNone(refresh_token.revoked_at)

    def test_expires_at(self):
        refresh_token = self.refresh_token_instance
        exp_delta = jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        expires_at = refresh_token.created_at + exp_delta

        self.assertEqual(refresh_token.expires_at, expires_at)

    def test_get_payload_by_token(self):
        refresh_token = self.refresh_token_instance
        payload = refresh_token.get_payload_by_token()

        self.assertIsNotNone(payload)

        for key in ['exp', 'sub', 'jti', 'type']:
            self.assertIn(key, payload)

        self.assertEqual(payload['type'], 'refresh')


class ResetTokenTest(UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.model = ResetToken
