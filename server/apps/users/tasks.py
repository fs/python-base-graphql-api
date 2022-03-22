from celery import shared_task
from server.apps.users.models import ResetToken
from server.celery import app, logger
from server.core.auth.jwt.models import RefreshToken


@shared_task(ignore_result=True)
def send_recovery_email(reset_token_pk):
    """Sending recovery email in background."""
    reset_token = ResetToken.objects.get(pk=reset_token_pk)
    if reset_token.is_active:
        reset_token.send_recovery_mail()


@app.task(ignore_result=True)
def clear_not_active_tokens(*args, **kwargs):
    """Clear not active tokens task."""
    RefreshToken.objects.delete_inactive_tokens()
    logger.info('Remove inactive tokens')
