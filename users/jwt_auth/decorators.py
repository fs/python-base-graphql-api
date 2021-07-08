from functools import partial, wraps

from graphql.execution.execute import GraphQLResolveInfo
from users.jwt_auth.exceptions import PermissionDenied


def find_context():
    """Find info(GraphQLResolveInfo instance) argument in resolvers or mutations and return context from that."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, GraphQLResolveInfo))
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def user_passes_test(test_func, exc=PermissionDenied):
    """Decorator factory."""
    def decorator(func):
        @wraps(func)
        @find_context
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return func(*args, **kwargs)
            raise exc

        return wrapper

    return decorator


def check_perms(user, perm):
    """Check user having permission."""
    if isinstance(perm, str):
        perms = (perm,)
    else:
        perms = perm
    return user.has_perms(perms)


def permission_required(perm):
    """Permission required decorator like in django."""
    func = partial(check_perms, perm=perm)
    return user_passes_test(func)


login_required = user_passes_test(lambda user: user.is_authenticated)
staff_member_required = user_passes_test(lambda user: user.is_staff)
superuser_required = user_passes_test(lambda user: user.is_superuser)
