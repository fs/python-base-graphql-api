from calendar import timegm
from datetime import datetime

from server.core.auth.jwt.utils import generate_hash


def generate_hash_for_user(user, created_at: datetime) -> str:
    """Generation hash with options for unique."""
    user_id = user.id
    timestamp = timegm(created_at.utctimetuple())

    key = f'{user_id}-{timestamp}'
    return generate_hash(key)
