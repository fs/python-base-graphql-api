
from server.settings.components.common import INSTALLED_APPS


DEBUG = True

INSTALLED_APPS += (  # noqa: F405
    # test apps with models
    'tests.test_server.test_core.test_graphql',
)
