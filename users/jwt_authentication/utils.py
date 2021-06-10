import jwt
import hashlib

from calendar import timegm
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
jwt_settings = settings.JWT_SETTINGS


def jwt_payload(user, expires, jti, token_type):
    return {
        "sub": user.id,
        "exp": timegm(expires.utctimetuple()),
        "jti": jti,
        "type": token_type,
    }


def get_user_by_access_token(token):
    payload = jwt_decode(token)

    if payload.get('exp') < timegm(datetime.utcnow().utctimetuple()):
        user_id = payload.get('sub')
        return User.objects.get(id=user_id)

    return None


def jwt_encode(payload):
    return jwt.encode(
        payload,
        jwt_settings.get('JWT_SECRET_KEY'),
        jwt_settings.get('JWT_ALGORITHM'),
    )


def jwt_decode(token):

    return jwt.decode(
        token,
        jwt_settings.get('JWT_SECRET_KEY'),
        options={
            'verify_exp': jwt_settings.get('JWT_VERIFY_EXPIRATION'),
            'verify_aud': jwt_settings.get('JWT_AUDIENCE') is not None,
            'verify_signature': jwt_settings.get('JWT_VERIFY'),
        },
        leeway=jwt_settings.get('JWT_LEEWAY'),
        audience=jwt_settings.get('JWT_AUDIENCE'),
        issuer=jwt_settings.get('JWT_ISSUER'),
        algorithms=[jwt_settings.get('JWT_ALGORITHM')],
    )


def get_access_token_by_request(request):
    auth = request.META.get(jwt_settings.get('JWT_AUTH_HEADER_NAME'), '').split()
    prefix = jwt_settings.get('JWT_AUTH_HEADER_PREFIX')

    if len(auth) != 2 or auth[0] != prefix:
        return None

    return auth[1]


def get_refresh_token_by_request(request):
    return request.META.get(jwt_settings.get('JWT_REFRESH_TOKEN_COOKIE_NAME'))


def set_cookie(response, key, value, expires):
    kwargs = {
        'expires': expires,
        'httponly': True,
        'secure': False,
        'path': '/',
        'domain': None,
        'samesite': None,
    }

    response.set_cookie(key, value, **kwargs)


def delete_cookie(response, key):
    response.delete_cookie(
        key,
        path='/',
        domain=None,
    )
