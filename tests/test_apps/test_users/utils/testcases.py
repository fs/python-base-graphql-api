from abc import ABC
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from hypothesis.extra.django import TestCase
from graphene.test import Client
from server.schema import schema

User = get_user_model()


class UserCreatedTestCase(ABC, TestCase):
    """Abstract TestCase with user creation and setting credentials."""

    def setUp(self):
        """Setup credentials."""
        super().setUp()
        self.email = 'test@test.test'
        self.password = 'test_password'

        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.user = user

class QueryTest(ABC, TestCase):
    """Abstract TestCase with user and Client creation."""

    def setUp(self):
        super().setUp()
        self.email = 'test_new@test.test'
        self.password = 'test_new_password'
        self.first_name = 'test'
        self.last_name = 'test'

        user = User.objects.create(email=self.email, first_name=self.first_name, last_name=self.last_name)
        user.set_password(self.password)
        user.save()
        self.graphql_client = Client(schema)

    def graphql_request(
            self,
            request_string,
            context=None,
            variables=None
    ):
        """GraphQl request for client with chosen schema."""
        if context is None:
            context = {}
        graphql_response = self.graphql_client.execute(request_string, variables=variables,
                                                       context=self.generate_context(**context))
        return graphql_response

    def generate_context(self, user=None, files=None):
        """Request context generating."""
        request = RequestFactory()
        context_value = request.get('/graphql')
        context_value.user = user or AnonymousUser()
        self.__set_context_files(context_value, files)
        return context_value

    @staticmethod
    def __set_context_files(context, files):
        """Context files setting."""
        if isinstance(files, dict):
            for name, file in files.items():
                context.FILES[name] = file
