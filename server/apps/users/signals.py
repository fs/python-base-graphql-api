from django.dispatch import Signal
from server.apps.users.models import UserActivity


def save_activity(user, activity, **kwargs):
    """Saving users activity to database. Used by signal."""
    UserActivity.objects.create(user=user, event=activity)


user_activity_signal = Signal()
user_activity_signal.connect(save_activity)
