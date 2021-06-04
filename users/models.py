from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


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
