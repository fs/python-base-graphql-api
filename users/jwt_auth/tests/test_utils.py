from datetime import timedelta
from django.utils import timezone
from users.jwt_auth import utils
from .testcases import UserAuthenticatedTestCase


class JWTTest(UserAuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.get_payload = utils.jwt_payload
        self.encode = utils.jwt_encode
        self.decode = utils.jwt_decode

    def get_payload_data(self):
        expires = timezone.now() + timedelta(hours=1)
        jti = utils.generate_hash('test')
        token_type = 'access'
        return {
            'user': self.user,
            'expires': expires,
            'jti': jti,
            'token_type': token_type
        }

    def test_generate_hash(self):
        result = utils.generate_hash('test')
        self.assertIsNotNone(result)

    def test_paylaod(self):

        jwt_payload = self.get_payload(**self.get_payload_data())

        for key in ['exp', 'sub', 'jti', 'type']:
            self.assertIn(key, jwt_payload)

        self.assertIsInstance(jwt_payload['exp'], int)

    def test_decode(self):
        payload = self.get_payload(**self.get_payload_data())
        token = self.encode(payload)
        decoded_payload = self.decode(token)
        self.assertEqual(payload, decoded_payload)

    def test_encode(self):
        payload = self.get_payload(**self.get_payload_data())
        token = self.encode(payload)
        self.assertIsNotNone(token)








