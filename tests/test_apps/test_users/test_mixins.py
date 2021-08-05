import unittest
from tests.test_apps.test_users.testcases import UserCreatedTestCase
from server.apps.users.mixins import (UpdateUserMixin, PasswordRecoveryMixin, UpdatePasswordMixin)
from server.core.authentication.jwt.exceptions import InvalidCredentials
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateUserMixinTest(UserCreatedTestCase):


    def test_change_password(self):
        new_password = 'new_test_password'
        UpdateUserMixin.change_password(self.user, self.password, new_password)
        self.assertTrue(self.user.check_password(new_password))
        self.assertFalse((self.user.check_password(self.password)))


    def test_check_valid_password_(self, ):
        new_password = 'new_test_password'
        invalid_password = 'invalid_password'
        with self.assertRaises(InvalidCredentials):
            UpdateUserMixin.change_password(self.user, invalid_password, new_password)

    def test_update_user_fields(self):
        new_user_fields = {
            'email': 'test_email@email.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
        }
        UpdateUserMixin.update_user_fields(self.user, new_user_fields)
        for field in new_user_fields:
            user_field_value = getattr(self.user, field)
            self.assertEqual(user_field_value, new_user_fields[field])

    def test_update_user(self):
        pass

class PasswordRecoveryMixinTest(UserCreatedTestCase):


    def test_recovery(self):
        pass

class UpdatePaswwordMixinTest(UserCreatedTestCase):

    def test_update_password(self):
        pass