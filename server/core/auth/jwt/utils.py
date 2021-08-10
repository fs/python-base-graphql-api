import hashlib
from calendar import timegm
from datetime import datetime
from typing import Dict, Literal, Union

import jwt
from django.conf import settings
from graphene.types.context import Context

jwt_settings = settings.JWT_SETTINGS


def jwt_payload(
    user,
    expires: datetime,
    jti: str,
    token_type: Literal['access', 'refresh'],
) -> Dict[str, Union[str, int]]:
    """Make dict with JWT params."""
    return {
        'sub': user.id,
        'exp': timegm(expires.utctimetuple()),
        'jti': jti,
        'type': token_type,
    }


def jwt_encode(payload: Dict[str, Union[str, int]]) -> str:
    """Encode payload to JWT token."""
    return jwt.encode(
        payload,
        jwt_settings.get('JWT_SECRET_KEY'),
        jwt_settings.get('JWT_ALGORITHM'),
    )


def jwt_decode(token: str) -> Dict[str, Union[str, int]]:
    """Decode token to payload."""
    return jwt.decode(
        token,
        jwt_settings.get('JWT_SECRET_KEY'),
        options={
            'verify_exp': jwt_settings.get('JWT_VERIFY_EXPIRATION'),
            'verify_signature': jwt_settings.get('JWT_VERIFY'),
        },
        algorithms=[jwt_settings.get('JWT_ALGORITHM')],
    )


def get_access_token_by_request(request: Context) -> str:
    """Get access token from request headers."""
    auth = request.META.get(jwt_settings.get('JWT_AUTH_HEADER_NAME'), '').split()
    prefix = jwt_settings.get('JWT_AUTH_HEADER_PREFIX')

    if len(auth) != 2 or auth[0] != prefix:
        return None

    return auth[1]


def get_access_payload_by_request(request: Context) -> Dict[str, Union[str, int]]:
    """Get token payload from request."""
    access_token = get_access_token_by_request(request)
    try:
        return jwt_decode(access_token)
    except jwt.exceptions.DecodeError:
        return None


def generate_hash(string: str) -> str:
    """Generate unique hash by string."""
    get_hash = hashlib.new('MD5')  # noqa: S324
    get_hash.update(string.encode('utf-8'))
    return get_hash.hexdigest()
