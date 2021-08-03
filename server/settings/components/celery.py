from server.settings.components.common import INSTALLED_APPS, TIME_ZONE

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = TIME_ZONE

INSTALLED_APPS += (
    'health_check.contrib.celery',
    'health_check.contrib.celery_ping',
    'health_check.contrib.redis',
)
