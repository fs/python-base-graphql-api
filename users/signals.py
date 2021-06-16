from django.dispatch import Signal
from .models import UserActivity


def save_activity(user, activity, **kwargs):
    UserActivity.objects.create(user=user, activity=activity)


user_activity_signal = Signal()
user_activity_signal.connect(save_activity)

