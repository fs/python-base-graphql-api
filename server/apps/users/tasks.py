from celery import shared_task
from server.apps.users.models import ResetToken
from server.celery import app, logger


@shared_task(ignore_result=True)
def send_recovery_email(reset_token_pk):
    """Sending recovery email in background."""
    reset_token = ResetToken.objects.get(pk=reset_token_pk)
    if reset_token.is_active:
        reset_token.send_recovery_mail()


@app.task(bind=True)
def clear_not_active_tokens(*args, **kwargs):
    """Sending recovery email in background."""
    ResetToken.objects.delete_inactive_tokens()
    logger.info('a+1')
