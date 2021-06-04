import graphene
from .inputs import SignInInput
from users.types import UserType
from django.contrib.auth import authenticate, login


class SignIn(graphene.Mutation):
    class Input:
        input = SignInInput()

    me = graphene.Field(UserType)

    @staticmethod
    def mutate(_, info, input):
        email = input.get('email')
        password = input.get('password')

        if email and password:
            user = authenticate(info.context, email=email, password=password)

        if not user:
            raise Exception('Wrong credentials')

        login(info.context, user)

        return SignIn(me=user)


class Mutation:
    signin = SignIn.Field(required=True)
