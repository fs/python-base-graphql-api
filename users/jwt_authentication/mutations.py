import graphql_jwt
import graphene

from graphql_jwt import Verify, Refresh
from .mixins import AuthenticationMixin
from .inputs import SignInInput


class SignIn(AuthenticationMixin, graphql_jwt.ObtainJSONWebToken, graphene.Mutation):

    class Arguments:
        input = SignInInput()

    class Meta(AuthenticationMixin.Meta):
        pass

    @classmethod
    def Field(cls, *args, **kwargs):
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    def mutate(cls, root, info, input):
        return super().mutate(root, info, **input)


class Mutation:
    sign_in = SignIn.Field(name='signin')
    test_verify = Verify.Field()
    test_refresh = Refresh.Field()
