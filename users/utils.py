from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model
from users.jwt_auth.utils import generate_hash

User = get_user_model()


def generate_hash_for_user(user: User, created_at: datetime) -> str:
    """Generation hash with options for unique."""
    user_id = user.id
    timestamp = timegm(created_at.utctimetuple())

    key = f'{user_id}-{timestamp}'
    return generate_hash(key)


def get_user_or_none(**kwargs) -> User:
    """Get user without exception."""
    try:
        return User.objects.get(**kwargs)
    except User.DoesNotExist:
        return None
