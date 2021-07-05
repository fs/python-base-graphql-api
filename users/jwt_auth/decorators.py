from functools import wraps

from graphql.execution.execute import GraphQLResolveInfo

from .exceptions import PermissionDenied


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(
                arg for arg in args
                if isinstance(arg, GraphQLResolveInfo)
            )
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def user_passes_test(test_func, exc=PermissionDenied):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exc

        return wrapper

    return decorator


login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return user.has_perms(perms)

    return user_passes_test(check_perms)