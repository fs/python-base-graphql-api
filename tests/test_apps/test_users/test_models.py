from django.test import TestCase
import unittest
from server.apps.users.models import UserManager, User, UserActivity
from server.apps.users.exceptions import UserAlreadyJoined


class UserManagerTest(TestCase):
    """Test UserManager model."""

    def setUp(self):
        """Setup model and instance of model."""
        self.user_manager = UserManager()

    def test_create_user_without_email(self):
        try:
            self.user_manager.create_user(email=None, password=None)
        except ValueError as ex:
            self.assertRaisesMessage(ex, 'The given email must be set')

    @unittest.expectedFailure
    def test_create_user(self):
        try:
            self.user_manager.create_user(email="test1@test.com",password="test")
        except Exception as ex:
            self.assertRaisesMessage(ex, UserAlreadyJoined())




