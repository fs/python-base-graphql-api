import graphene
from ..types import UserType


class AuthenticationMixin:

    class Meta:
        name = 'Authentication'

    token = graphene.String()
    me = graphene.Field(UserType)
    refresh_token = graphene.String(name='refreshToken')

    @staticmethod
    def resolve_me(_, info):
        return info.context.user

    @staticmethod
    def resolve_refresh_token(obj, info):

        return "LOL"


