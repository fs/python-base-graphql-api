import graphene
from ..types import UserType


class AuthenticationOutput(graphene.ObjectType):

    class Meta:
        name = 'Authentication'

    token = graphene.String(name='accessToken')
    me = graphene.Field(UserType)
    refresh_token = graphene.String(name='refreshToken')

    @staticmethod
    def resolve_me(_, info):
        return info.context.user


class SignOutOutput(graphene.ObjectType):
    class Meta:
        name = 'Message'

    message = graphene.String()



