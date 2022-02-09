from server.settings.components.common import INSTALLED_APPS, TIME_ZONE, config

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_TIMEZONE = TIME_ZONE

INSTALLED_APPS += (
    'health_check.contrib.celery',
    'health_check.contrib.celery_ping',
    'health_check.contrib.redis',
)

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
