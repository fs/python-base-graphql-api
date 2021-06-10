from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import jwt_encode
from .models import RefreshToken

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class ObtainPairMixin:

    @classmethod
    def generate_pair(cls, user):
        refresh_token = RefreshToken.objects.create(user=user)
        access_payload = refresh_token.get_payload_by_token()
        access_payload['type'] = 'access'
        access_token = jwt_encode(access_payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token.token,
        }


class RevokeAccessTokenMixin:
    def logout(self, request, everywhere=False):
        if everywhere:
            RefreshToken.objects.revoke_all_for_user(request.user)
        else:
            request.refresh_token.revoke()


class UpdateAccessTokenMixin(ObtainPairMixin):

    @classmethod
    def update_access_token(cls, request):
        request.refresh_token.revoke()
        return cls.generate_pair(request.user)








