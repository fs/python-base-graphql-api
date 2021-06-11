from pathlib import Path
from decouple import config
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', config('DOMAIN_NAME')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'users.jwt_authentication',
    'users',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base_graphql_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base_graphql_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),

    }
}

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.jwt_authentication.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPHENE = {
    'SCHEMA': 'base_graphql_api.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        'users.jwt_authentication.middleware.TokenAuthenticationMiddleware',
        # 'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

JWT_SETTINGS = {
    'REFRESH_TOKEN_EXPIRATION_DELTA': timedelta(days=30),
    'ACCESS_TOKEN_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_REFRESH_TOKEN_COOKIE_NAME': 'refreshToken',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_AUDIENCE': None,
    'JWT_VERIFY': True,
    'JWT_ISSUER': None,
    'JWT_LEEWAY': 0,
}

AWS_ACCESS_KEY_ID = config('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('S3_BUCKET_NAME')
AWS_S3_REGION_NAME = config('S3_BUCKET_REGION')
AWS_S3_MAX_MEMORY_SIZE = 10 * 1024 * 1024
