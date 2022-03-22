from datetime import timedelta

from server.settings.components import config

JWT_SETTINGS = {
    'REFRESH_TOKEN_EXPIRATION_DELTA': timedelta(days=30),
    'ACCESS_TOKEN_EXPIRATION_DELTA': timedelta(hours=1),
    'TOKEN_GRACE_PERIOD': timedelta(minutes=1),
    'JWT_AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_REFRESH_TOKEN_COOKIE_NAME': 'refreshToken',
    'JWT_SECRET_KEY': config('SECRET_KEY'),
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_VERIFY': True,
}
