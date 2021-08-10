from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from server.apps.users.exceptions import UserAlreadyJoined
from server.apps.users.storages import S3DirectUploadStorage
from server.apps.users.utils import send_recovery_email
from server.core.auth import utils as user_utils


class UserManager(DjangoUserManager):
    """Custom queryset for User model."""

    def create_user(self, email, **extra_fields):
        """Changed from username to email."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if User.objects.filter(email=email).exists():
            raise UserAlreadyJoined()

        return self._create_user(email, **extra_fields)

    def get_user_or_none(self, **kwargs):
        """Get user without exception."""
        try:
            return self.get(**kwargs)

        except self.model.DoesNotExist:
            return None

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Override for email as username support."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """Override for email as username support. Saved normalizing for login field."""
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)  # noqa: N806, WPS437
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(null=True, blank=True, storage=S3DirectUploadStorage())

    objects = UserManager()

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []


class UserActivity(models.Model):
    """User activity logging in DB."""

    USER_LOGGED_IN = 'USER_LOGGED_IN'
    USER_REGISTERED = 'USER_REGISTERED'
    USER_RESET_PASSWORD = 'USER_RESET_PASSWORD'
    RESET_PASSWORD_REQUESTED = 'RESET_PASSWORD_REQUESTED'
    USER_UPDATED = 'USER_UPDATED'

    EVENT_CHOICES = (
        (USER_LOGGED_IN, 'User logged id'),
        (USER_REGISTERED, 'User registered'),
        (USER_RESET_PASSWORD, 'User reset password'),
        (RESET_PASSWORD_REQUESTED, 'Reset password requested'),
        (USER_UPDATED, 'User updated'),
    )

    event = models.CharField(max_length=255, choices=EVENT_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User activity'
        verbose_name_plural = 'User activities'

    def __str__(self):
        return self.event


class ResetTokenQuerySet(models.QuerySet):
    """Reset token QuerySet."""

    def get_active_token(self, token: str):
        """Get active token."""
        expires_at_by_now = timezone.now() - settings.PASS_RESET_TOKEN_EXPIRATION_DELTA
        return self.get(created_at__gt=expires_at_by_now, token=token)


ResetTokenManager = models.Manager.from_queryset(ResetTokenQuerySet)


class ResetToken(models.Model):  # noqa: D101
    token = models.CharField(max_length=255, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reset_tokens')

    objects = ResetTokenManager()

    class Meta:
        verbose_name = 'Reset token'
        verbose_name_plural = 'Reset tokens'

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        """created_at and token generation."""
        if not self.created_at:
            self.created_at = timezone.now()

        if not self.token:
            self.token = user_utils.generate_hash_for_user(self.user, self.created_at)

        return super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        """Check token is expired."""
        return timezone.now() > (self.created_at + settings.PASS_RESET_TOKEN_EXPIRATION_DELTA)

    @property
    def is_active(self) -> bool:
        """Check token is not expired and not used."""
        return not (self.is_expired or self.is_used)

    def set_password(self, password):
        """Password setting for user."""
        self.is_used = True
        self.user.set_password(password)

    def send_recovery_mail(self):
        """Send email to user with instructions."""
        send_recovery_email(
            self.user.first_name,
            self.user.last_name,
            self.token,
            self.user.email,
        )
