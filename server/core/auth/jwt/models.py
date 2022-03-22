from typing import Dict, NoReturn, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from server.core.auth import utils as user_utils
from server.core.auth.jwt import utils

jwt_settings = settings.JWT_SETTINGS
User = get_user_model()


class RefreshTokenQuerySet(models.QuerySet):
    """Methods for comfort work with refresh tokens."""

    def revoke_all_for_user(self, user: User):
        """Revoking all tokens for user."""
        self.get_active_tokens_for_sub(user.id).update(revoked_at=timezone.now())

    def delete_inactive_tokens(self):
        """Delete all inactive tokens."""
        self.filter_inactive_tokens().delete()

    def get_active_tokens_for_sub(self, sub: Union[str, int], **kwargs):
        """Filter active tokens for JWT sub(user id)."""
        return self.filter_active_tokens(user__id=sub, **kwargs)

    def filter_active_tokens(self, **kwargs):
        """Filter all active tokens."""
        now = timezone.now()
        expires_at_by_now = now - jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        return self.filter(
            models.Q(created_at__gt=expires_at_by_now) &
            (
                models.Q(revoked_at__gt=now) |
                models.Q(revoked_at__isnull=True)
            ) &
            models.Q(**kwargs),
        )

    def filter_inactive_tokens(self, **kwargs):
        """Filter not active tokens."""
        now = timezone.now()
        expires_at_by_now = now - jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')
        return self.exclude(
            models.Q(created_at__lt=expires_at_by_now) |
            models.Q(revoked_at__lt=now) &
            models.Q(**kwargs),
        )

    def access_token_is_active(self, jti: str, **kwargs) -> bool:
        """Check tokens is active by JTI. Usually uses for access token revoking check."""
        return self.filter_active_tokens(jti=jti, **kwargs).exists()


RefreshTokenManager = models.Manager.from_queryset(RefreshTokenQuerySet)


class RefreshToken(models.Model):  # noqa: D101
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    jti = models.CharField(max_length=255, editable=False)
    token = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    parent_token = models.OneToOneField(
        'RefreshToken',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='substitution_token',
        default=None,
    )

    objects = RefreshTokenManager()

    class Meta:
        unique_together = ('token', 'created_at', 'jti')
        verbose_name = 'Refresh token'
        verbose_name_plural = 'Refresh tokens'

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        """Fields generation in save time."""
        if not self.created_at:
            self.created_at = timezone.now()

        if not self.jti:
            self.jti = user_utils.generate_hash_for_user(self.user, self.created_at)

        if not self.token:
            payload = utils.jwt_payload(self.user, self.expires_at, self.jti, 'refresh')
            self.token = utils.jwt_encode(payload)

        return super().save(*args, **kwargs)

    @property
    def expires_at(self):
        """Compute expires at datetime."""
        return self.created_at + jwt_settings.get('REFRESH_TOKEN_EXPIRATION_DELTA')

    @property
    def is_expired(self) -> bool:
        """Refresh token expires."""
        return self.expires_at < timezone.now()

    @property
    def is_revoked(self) -> bool:
        """Check is token revoked."""
        return self.revoked_at is not None and self.revoked_at < timezone.now()

    @property
    def is_active(self) -> bool:
        """Check refresh token is active: is not revoked and not expired."""
        return not (self.is_revoked or self.is_expired)

    def get_payload_by_token(self) -> Dict[str, Union[int, str]]:
        """Token decoding by JWT algorithm."""
        return utils.jwt_decode(self.token)

    def revoke(self) -> NoReturn:
        """Revoke refresh token."""
        self.revoked_at = timezone.now()
        self.save()

    def prolong_grace_period(self) -> NoReturn:
        """Prolong token grace period."""
        self.revoked_at = timezone.now() + jwt_settings.get('TOKEN_GRACE_PERIOD')
        self.save()
