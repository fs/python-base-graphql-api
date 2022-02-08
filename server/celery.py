import logging
import os

from celery import Celery
from celery.schedules import crontab

logger = logging.getLogger('django')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'run-every-afternoon': {
        'task': 'tasks.clear_not_active_tokens',
        'schedule': crontab(hour=14, minute=43),
        'args': (),
    },
}


@app.task(bind=True)
def debug_task(self):
    """Task for view debug messages."""
    message = f'Request: {self.request!r}'
    logger.debug(message)
