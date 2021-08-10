from server.settings.components import config
from server.settings.components.common import INSTALLED_APPS

AWS_ACCESS_KEY_ID = config('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('S3_BUCKET_NAME')
AWS_S3_REGION_NAME = config('S3_BUCKET_REGION')
AWS_S3_MAX_MEMORY_SIZE = 10 * 1024 * 1024

INSTALLED_APPS += (
    'health_check.storage',
    'health_check.contrib.s3boto3_storage',
)
