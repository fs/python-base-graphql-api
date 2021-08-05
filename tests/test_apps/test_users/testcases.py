from abc import ABC

from unittest import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreatedTestCase(ABC, TestCase):
    """Abstract TestCase with set credentials."""

    def setUp(self):
        """Setup credentials."""
        self.email = 'test123@test.test'
        self.password = 'test_password'

        user = User.objects.create(email=self.email)
        user.set_password(self.password)

        self.user = user


