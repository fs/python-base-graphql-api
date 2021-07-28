from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from server.apps.users.exceptions import UserAlreadyJoined
from server.apps.users.storages import S3DirectUploadStorage


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
