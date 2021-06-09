import graphql_jwt
import graphene

from graphql_jwt.shortcuts import create_refresh_token, get_token
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from .outputs import AuthenticationOutput, SignOutOutput
from .inputs import SignInInput, SignUpInput, SignOutInput

User = get_user_model()


class SignIn(graphql_jwt.ObtainJSONWebToken, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignInInput(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    def mutate(cls, root, info, input):
        return super().mutate(root, info, **input)


class SignUp(graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignUpInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        user = User.objects.create_user(**input)

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        info.context.user = user

        return cls.Output(me=user, token=token, refresh_token=refresh_token)


class SignOut(graphene.Mutation):
    Output = SignOutOutput

    class Arguments:
        input = SignOutInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        everywhere = input.get('everywhere')
        if everywhere:
            for token in info.context.user.jwt_refresh_tokens.all():
                token.revoke()
        else:
            info.context.jwt_refresh_token.revoke()
        return cls.Output(message="Success")


class UpdateToken(graphql_jwt.Refresh, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        pass

    @classmethod
    def mutate(cls, root, info):
        return super(UpdateToken, cls).mutate(root, info)


class Mutation:
    sign_in = SignIn.Field(name='signin')
    sign_up = SignUp.Field(name='signup')
    sign_out = SignOut.Field(name='signout')
    update_token = UpdateToken.Field(name='updateToken')


