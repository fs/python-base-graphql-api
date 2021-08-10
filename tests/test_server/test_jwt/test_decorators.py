from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from server.core.auth.jwt import decorators
from server.core.auth.jwt.exceptions import PermissionDenied
from tests.test_server.test_jwt.testcases import UserAuthenticatedTestCase

User = get_user_model()


class DecoratorTestMixin:
    """Abstract universal decorator test."""

    user_with_perms = None
    user_without_perms = None
    decorator = None

    def test_permission_denied(self):
        """Make conditions for permission denied exception raising."""
        func = self.decorator(lambda info: None)
        with self.assertRaises(PermissionDenied):
            func(self.info(self.user_without_perms))

    def test_permission_accept(self):
        """Make conditions for accepting request."""
        func = self.decorator(lambda info: None)
        decorator_result = func(self.info(self.user_with_perms))
        self.assertIsNone(decorator_result)


class UserPassesTests(UserAuthenticatedTestCase):
    """Test making decorators from user_passes_test."""

    def setUp(self):
        """Setup decorator."""
        self.decorator = decorators.user_passes_test
        super().setUp()

    def test_decorator(self):
        """Test user_passes_test with lambda."""
        decorator = self.decorator(lambda user: user.pk == self.user.pk)
        decorated_func = decorator(lambda info: None)
        request_handle_result = decorated_func(self.info(user=self.user))
        self.assertEqual(request_handle_result, None)

    def test_decorator_raise(self):
        """Test give custom exception argument."""
        custom_exc = type('TestException', (Exception,), {'message': 'test'})
        decorator = self.decorator(lambda user: user.pk != user.pk, exc=custom_exc)
        decorated_func = decorator(lambda info: None)

        with self.assertRaises(custom_exc):
            decorated_func(self.info(user=self.user))


class LoginRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    """Testing info.context.user.is_authenticated decorator."""

    def setUp(self):
        """Setup user_with_perms - authenticated user, user_without_perms - AnonymousUser."""
        super().setUp()
        self.decorator = decorators.login_required
        self.user_with_perms = self.user
        self.user_without_perms = AnonymousUser()


class StaffMemberRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    """Testing info.context.user.is_staff decorator."""

    def setUp(self):
        """Setup user_with_perms - user with active is_staff attr, user_without_perms - default user."""
        super().setUp()
        self.decorator = decorators.staff_member_required
        self.user_without_perms = self.user
        self.user_with_perms = User.objects.create(email='staffmember@test.test')
        self.user_with_perms.is_staff = True
        self.user_with_perms.save()


class SuperuserRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    """Testing info.context.user.is_superuser decorator."""

    def setUp(self):
        """Setup user_with_perms - new superuser, user_without_perms - default user."""
        super().setUp()
        self.decorator = decorators.superuser_required
        self.user_without_perms = self.user
        self.user_with_perms = User.objects.create_superuser(email='superuser@test.test')
