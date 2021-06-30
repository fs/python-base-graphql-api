from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from users.jwt_authentication import decorators
from .testcases import UserAuthenticatedTestCase
from ..exceptions import PermissionDenied

User = get_user_model()


class DecoratorTestMixin:
    user_with_perms = None
    user_without_perms = None
    decorator = None

    def test_permission_denied(self):
        func = self.decorator(lambda info: None)
        with self.assertRaises(PermissionDenied):
            func(self.info(self.user_without_perms))

    def test_permission_accept(self):
        func = self.decorator(lambda info: None)
        result = func(self.info(self.user_with_perms))
        self.assertEqual(result, None)


class UserPassesTests(UserAuthenticatedTestCase):
    def setUp(self):
        self.decorator = decorators.user_passes_test
        super(UserPassesTests, self).setUp()

    def test_decorator(self):
        func = self.decorator(lambda user: user.pk == self.user.pk)(lambda info: None)
        result = func(self.info(user=self.user))
        self.assertEqual(result, None)

    def test_decorator_raise(self):
        custom_exc = type("TestException", (Exception,), {'message': 'test'})
        func = self.decorator(lambda user: user.pk != user.pk, exc=custom_exc)(lambda info: None)

        with self.assertRaises(custom_exc):
            func(self.info(user=self.user))


class LoginRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.decorator = decorators.login_required
        self.user_with_perms = self.user
        self.user_without_perms = AnonymousUser()


class StaffMemberRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()

        self.decorator = decorators.staff_member_required
        self.user_without_perms = self.user

        self.user_with_perms = User.objects.create(email='staffmember@test.test')
        self.user_with_perms.is_staff = True
        self.user_with_perms.save()


class SuperUserMemberRequiredTest(DecoratorTestMixin, UserAuthenticatedTestCase):
    def setUp(self):
        super().setUp()

        self.decorator = decorators.superuser_required
        self.user_without_perms = self.user

        self.user_with_perms = User.objects.create_superuser(email='superuser@test.test')
