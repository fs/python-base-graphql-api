"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""
import django_heroku
from server.settings.components import config

# Production flags:
# https://docs.djangoproject.com/en/3.2/howto/deployment/

DEBUG = False

ALLOWED_HOSTS = [
    # TODO: check production hosts
    config('DOMAIN_NAME'),

    # We need this value for `healthcheck` to work:
    'localhost',
]


django_heroku.settings(locals())
