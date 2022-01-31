
from server.settings.environments.development import *  # noqa: F403, WPS347

DEBUG = True

INSTALLED_APPS += (  # noqa: F405
    # test apps with models
    'tests.test_server.test_core.test_graphql',
)
