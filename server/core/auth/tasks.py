from server.celery import app
from server.apps.users.models import ResetToken


@app.task()
def clear_not_active_tokens():
    """Sending recovery email in background."""
    ResetToken.objects.delete_inactive_tokens()
    print('Reset tokens deleted')
