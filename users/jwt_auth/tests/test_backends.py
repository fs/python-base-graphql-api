from django.conf import settings

from .testcases import UserAuthenticatedTestCase
from ..backends import JSONWebTokenBackend
from ..exceptions import PermissionDenied

jwt_settings = settings.JWT_SETTINGS


class BackendTest(UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.backend = JSONWebTokenBackend()

    @staticmethod
    def get_auth_headers(access_token):
        access_token_header = jwt_settings.get('JWT_AUTH_HEADER_NAME')
        access_token_prefix = jwt_settings.get("JWT_AUTH_HEADER_PREFIX")
        return {
            access_token_header: f'{access_token_prefix} {access_token}',
        }

    def test_authenticate(self):
        headers = self.get_auth_headers(self.access_token)
        request = self.info(headers=headers).context
        user = self.backend.authenticate(request)
        self.assertIsNotNone(user)
        self.assertEqual(self.user, user)

    def test_revoked_refresh_token(self):
        info = self.get_authenticated_info_context()
        self.user.refresh_tokens.revoke_all_for_user(self.user)

        user = self.backend.authenticate(info.context)
        self.assertIsNone(user)

    def test_authenticate_invalid(self):
        request = self.get_authenticated_info_context(access_token='INVALID_ACCESS_TOKEN').context

        with self.assertRaises(PermissionDenied):
            self.backend.authenticate(request)

    def test_authenticate_null_request(self):
        user = self.backend.authenticate(request=None)
        self.assertIsNone(user)

    def test_get_user(self):
        user = self.backend.get_user(self.user.pk)
        self.assertIsNone(user)
