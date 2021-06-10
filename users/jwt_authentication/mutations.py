import graphene

from django.contrib.auth import authenticate, get_user_model, login

from .inputs import SignInInput, SignUpInput, SignOutInput
from .outputs import AuthenticationOutput, SignOutOutput
from .mixins import ObtainPairMixin

User = get_user_model()


class SignIn(ObtainPairMixin, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignInInput()

    @classmethod
    def mutate(cls, _, info, input):
        user = authenticate(info.context, **input)
        tokens = cls.generate_pair(user)
        return cls.Output(me=user, **tokens)


class SignUp(ObtainPairMixin, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignUpInput()

    @classmethod
    def mutate(cls, _, info, input):
        user = User.objects.create(**input)
        tokens = cls.generate_pair(user)
        return cls.Output(me=user, **tokens)


class SignOut(graphene.Mutation):
    Output = SignOutOutput

    class Arguments:
        input = SignOutInput()

    @classmethod
    def mutate(cls, _, info, input):
        everywhere = input.get('everywhere')


class Mutation:
    sign_in = SignIn.Field(name='signin')
    sign_up = SignUp.Field(name='signup')


