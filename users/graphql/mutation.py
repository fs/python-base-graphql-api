import graphql_jwt
import graphene
from .inputs import SignInInput
from .types import UserType
from django.contrib.auth import authenticate, login


class SignIn(graphene.Mutation):
    class Input:
        input = SignInInput()

    me = graphene.Field(UserType)

    @staticmethod
    def mutate(info, input):
        email = input.get('email')
        password = input.get('password')

        if email and password:
            user = authenticate(info.context.request, email=email, password=password)

        if not user:
            raise Exception('Wrong credentials')

        login(info.context.request, user)

        return SignIn(me=user)


class Mutation:
    signin = SignIn.Field(required=True)
