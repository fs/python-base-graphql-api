import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .types import UserType, UserActivityType
from users.jwt_authentication.decorators import login_required
from users.graphql.filters import UserActivityFilterSet
from ..models import UserActivity


class Query:
    activities = DjangoFilterConnectionField(UserActivityType, filterset_class=UserActivityFilterSet)
    # activity = graphene.relay.Node.Field(UserActivityType)
    me = graphene.Field(UserType)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        return info.context.user

