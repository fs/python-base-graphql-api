from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.aws_images_storage import AvatarStorage
from django.conf import settings


class UserQuerySet(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if User.objects.filter(email=email).exists():
            raise Exception('Already joined')

        return self._create_user(email, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(null=True, blank=True, storage=AvatarStorage())

    objects = UserQuerySet()

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []

    def save_image(self, folder, filename):
        self.avatar.name = f'{folder}/{filename}'
        self.save()


class UserActivity(models.Model):
    USER_LOGGED_IN = 'USER_LOGGED_IN'
    USER_REGISTERED = 'USER_REGISTERED'
    USER_RESET_PASSWORD = 'USER_RESET_PASSWORD'
    RESET_PASSWORD_REQUESTED = 'RESET_PASSWORD_REQUESTED'
    USER_UPDATED = 'USER_UPDATED'

    ACTIVITY_CHOICES = (
        (USER_LOGGED_IN, 'Пользователь вошел'),
        (USER_REGISTERED, 'Пользователь зарегестрировался'),
        (USER_RESET_PASSWORD, 'Пользователь восстановил пароль'),
        (RESET_PASSWORD_REQUESTED, 'Пользователь запросил смену пароля'),
        (USER_UPDATED, 'Пользователь обновлен')
    )

    activity = models.CharField(max_length=255, choices=ACTIVITY_CHOICES)
