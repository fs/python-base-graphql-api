from tests.test_apps.test_users.utils.testcases import UserCreatedTestCase
from server.apps.users.models import UserManager, User, UserActivity
from server.apps.users.exceptions import UserAlreadyJoined


class UserManagerTest(UserCreatedTestCase):
    """Test UserManager model."""

    def setUp(self):
        """Setup model and instance of model."""
        super().setUp()
        self.user_manager = UserManager()

    def test_create_user_without_email(self):
        """Test user creation without email."""
        with self.assertRaises(Exception):
            self.user_manager.create_user(email=None)

    def test_create_existing_user(self):
        """Test existing user creation."""
        with self.astestssertRaises(UserAlreadyJoined):
            self.user_manager.create_user(email=getattr(self.user, 'email'))





