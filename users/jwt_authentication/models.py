from calendar import timegm
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from .utils import jwt_encode, jwt_decode, jwt_payload, generate_hash
from django.conf import settings
from django.utils import timezone

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class RefreshTokenQuerySet(models.QuerySet):

    def revoke_all_for_user(self, user):
        self.filter(user=user).update(revoked_at=datetime.now())

    def get_active_tokens_for_user(self, sub):
        created_at = timezone.now() - jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        return self.filter(created_at__gt=created_at, revoked_at=None, user__id=sub)


class RefreshToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    jti = models.CharField(max_length=255, editable=False)
    token = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    objects = RefreshTokenQuerySet.as_manager()

    class Meta:
        unique_together = ('token', 'created_at', 'jti')

    def __str__(self):
        return self.token

    @property
    def expires_at(self):
        return self.created_at + jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')

    @property
    def is_expired(self):
        return self.expires_at > datetime.now()

    @property
    def is_revoked(self):
        return self.revoked_at is not None

    @property
    def is_active(self):
        return not (self.is_revoked or self.is_expired)

    def get_payload_by_token(self):
        return jwt_decode(self.token)

    @staticmethod
    def generate_jti(user, created_at):
        key = f'{user.id}-{timegm(created_at.utctimetuple())}'
        return generate_hash(key)

    def revoke(self):
        self.revoked_at = datetime.now()
        self.save()

    def save(self, *args, **kwargs):

        self.created_at = timezone.now()

        if not self.jti:
            self.jti = self.generate_jti(self.user, self.created_at)

        if not self.token:
            payload = jwt_payload(self.user, self.expires_at, self.jti, 'refresh')
            self.token = jwt_encode(payload)

        return super().save(*args, **kwargs)






