from datetime import datetime
from calendar import timegm

from graphql_jwt.settings import jwt_settings


def get_refresh_token_payload(created_at):
    exp = created_at + jwt_settings.JWT_EXPIRATION_DELTA

    payload = {
        "exp": timegm(exp.utctimetuple()),
        "origIat": timegm(created_at.utctimetuple()),
    }

    if jwt_settings.JWT_AUDIENCE is not None:
        payload['aud'] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload['iss'] = jwt_settings.JWT_ISSUER

    return payload
