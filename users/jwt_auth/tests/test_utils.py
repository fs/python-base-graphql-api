from datetime import timedelta

from django.utils import timezone
from users.jwt_auth import utils
from users.jwt_auth.tests import testcases


class JWTTest(testcases.UserAuthenticatedTestCase):
    """Tests for JWT token working."""

    def setUp(self):
        """Setup payload definition, hash generating, tokens encode and decode funcs."""
        super().setUp()
        self.get_payload = utils.jwt_payload
        self.encode = utils.jwt_encode
        self.decode = utils.jwt_decode
        self.generate_hash = utils.generate_hash

    def get_payload_data(self):
        """Make test payload data."""
        expires = timezone.now() + timedelta(hours=1)
        jti = utils.generate_hash('test')
        token_type = 'access'
        return {
            'user': self.user,
            'expires': expires,
            'jti': jti,
            'token_type': token_type,
        }

    def test_generate_hash(self):
        """Test for hash generating."""
        generated_hash = self.generate_hash('test')
        self.assertIsNotNone(generated_hash)

    def test_payload(self):
        """Test payload definition with check JWT params."""
        jwt_payload = self.get_payload(**self.get_payload_data())
        keys = ['exp', 'sub', 'jti', 'type']
        for key in keys:
            self.assertIn(key, jwt_payload)

        self.assertIsInstance(jwt_payload['exp'], int)

    def test_decode(self):
        """Test payload decoding from JWT token."""
        payload = self.get_payload(**self.get_payload_data())
        token = self.encode(payload)
        decoded_payload = self.decode(token)
        self.assertEqual(payload, decoded_payload)

    def test_encode(self):
        """Test JWT payload encoding to token."""
        payload = self.get_payload(**self.get_payload_data())
        token = self.encode(payload)
        self.assertIsNotNone(token)
