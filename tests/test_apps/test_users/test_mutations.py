from django.contrib.auth import get_user_model
from .utils.testcases import QueryTest
from .utils import requests
from server.core.authentication.jwt.exceptions import InvalidCredentials
from server.apps.users.exceptions import UserAlreadyJoined
from hypothesis import example, settings, given, strategies as st

User = get_user_model()


class SignInTest(QueryTest):

    def test_sign_in_with_valid_credentials(self):
        response = self.graphql_request(
            request_string=requests.SIGN_IN_MUTATION,
            variables={"email": self.email, "password": self.password},
        )
        self.assertEqual(response['data']['signin']['me']['email'], self.email)
        self.assertEqual(response['data']['signin']['me']['firstName'], self.first_name)
        self.assertEqual(response['data']['signin']['me']['lastName'], self.last_name)

    def test_sign_in_with_invalid_email(self):
        invalid_email = 'invalid@email.email'
        response = self.graphql_request(
            request_string=requests.SIGN_IN_MUTATION,
            variables={"email": invalid_email, "password": self.password},
        )
        self.assertEqual(response['errors'][0]['message'], InvalidCredentials.default_message)

    def test_sign_in_with_invalid_password(self):
        invalid_password = 'invalid_password'
        response = self.graphql_request(
            request_string=requests.SIGN_IN_MUTATION,
            variables={"email": self.email, "password": invalid_password},
        )
        self.assertEqual(response['errors'][0]['message'], InvalidCredentials.default_message)

    def test_sign_out(self):
        response = self.graphql_request(
            request_string=requests.SIGN_OUT_MUTATION,
            variables={"everywhere": True},
        )
        self.assertEqual(response['data']['signout']['message'], 'Success')

    @settings(max_examples=5)
    @given(st.emails(), st.text())
    def test_sign_up_with_valid_credentials(self, emails, text):
        emails = emails.lower()
        response = self.graphql_request(
            request_string=requests.SIGN_UP_MUTATION,
            variables={"email": emails, "password": self.password, "lastName": text, "firstName": text},
        )
        self.assertEqual(response['data']['signup']['me']['email'], emails)
        self.assertEqual(response['data']['signup']['me']['firstName'], text)
        self.assertEqual(response['data']['signup']['me']['lastName'], text)

    def test_sign_up_with_empty_email(self):
        response = self.graphql_request(
            request_string=requests.SIGN_UP_MUTATION,
            variables={"email": "", "password": '', "lastName": '', "firstName": ''},
        )
        self.assertEqual(response['errors'][0]['message'], 'The given email must be set')

    def test_sign_up_with_joined_user_email(self):
        response = self.graphql_request(
            request_string=requests.SIGN_UP_MUTATION,
            variables={"email": self.email, "password": 'test', "lastName": '', "firstName": ''},
        )
        self.assertEqual(response['errors'][0]['message'], UserAlreadyJoined.default_message)
