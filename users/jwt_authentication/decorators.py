from functools import wraps
from datetime import datetime

from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import set_cookie, delete_cookie


def jwt_refresh_token_cookie(view_func):

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        request.jwt_cookie = True
        response = view_func(request, *args, **kwargs)

        if hasattr(request, 'jwt_refresh_token'):
            refresh_token = request.jwt_refresh_token
            expires = refresh_token.created +\
                jwt_settings.JWT_REFRESH_EXPIRATION_DELTA

            set_cookie(
                response,
                jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
                refresh_token.token,
                expires=expires,
            )

        if hasattr(request, 'delete_refresh_token_cookie'):
            delete_cookie(response, jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME)

        return response
    return wrapped_view
