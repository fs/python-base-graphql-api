# Graphene settings


GRAPHENE = {
    'SCHEMA': 'server.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        'server.core.authentication.jwt.middleware.TokenAuthenticationMiddleware',
    ],
}
