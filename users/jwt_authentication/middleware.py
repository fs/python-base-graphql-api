from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

jwt_settings = settings.JWT_SETTINGS


class TokenAuthenticationMiddleware:

    def resolve(self, next, root, info, **kwargs):
        context = info.context

        user = authenticate(context)

        context.user = user or AnonymousUser()
        return next(root, info, **kwargs)
