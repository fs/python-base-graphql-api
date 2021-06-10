from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from .utils import jwt_encode, jwt_decode, jwt_payload
from django.conf import settings

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class RefreshTokenQuerySet(models.QuerySet):

    def create(self, user, expires_at=None, now=None):
        if not expires_at:

            if not now:
                now = datetime.now()

            expires_at = now + jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')

        payload = jwt_payload(user=user, expires=expires_at, token_type='refresh')
        token = jwt_encode(payload)
        return super(RefreshTokenQuerySet, self).create(user=user, token=token, expires_at=expires_at)

    def get_active_tokens(self):
        now = datetime.now()
        return self.filter(expires_at__lt=now)


class RefreshToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    jti = models.CharField(max_length=255, editable=False)
    token = models.CharField(max_length=255, editable=False)
    expires_at = models.DateTimeField()

    objects = RefreshTokenQuerySet.as_manager()

    class Meta:
        unique_together = ('token', 'expires_at')

    def __str__(self):
        return self.token

    @property
    def is_expired(self):
        return self.expires_at > datetime.now()

    def get_payload_by_token(self):
        return jwt_decode(self.token)

    def reuse(self, access_token):
        now = datetime.now()
        expires_at = now + jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        refresh_payload = jwt_payload(user=self.user, expires=expires_at, token_type='refresh')
        refresh_token = jwt_encode(refresh_payload)

        access_payload = jwt_decode()

        self.expires_at = expires_at
        self.token = refresh_token
        self.save()




