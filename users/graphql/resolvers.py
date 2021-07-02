import graphene

from graphql_core.connection_fields import FilterConnectionField
from users.graphql.filters import UserActivityFilterSet
from users.jwt_auth.decorators import login_required
from .types import UserType, UserActivityType
from ..models import UserActivity


class Query:
    activities = FilterConnectionField(UserActivityType, filterset_class=UserActivityFilterSet)
    activity = graphene.relay.Node.Field(UserActivityType)
    me = graphene.Field(UserType)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        return info.context.user
