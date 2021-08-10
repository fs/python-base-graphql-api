# Graphene settings


GRAPHENE = {
    'SCHEMA': 'server.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        'server.core.auth.jwt.middleware.TokenAuthenticationMiddleware',
    ],
}
