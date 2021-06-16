import graphene
from .relay import ActivityConnection
from graphene_django import DjangoConnectionField
from .types import UserType, UserActivityType
from .jwt_authentication.decorators import login_required


class Query:
    activities = graphene.DjangoConnectionField(UserActivityType)
    me = graphene.Field(UserType)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        return info.context.user

