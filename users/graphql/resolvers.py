import graphene
from graphql_core.connection_fields import FilterConnectionField
from users.graphql.filters import UserActivityFilterSet
from users.graphql.types import UserActivityType, UserType
from users.jwt_auth.decorators import login_required


class Query(object):
    """Users main GraphQL Query."""

    activities = FilterConnectionField(UserActivityType, filterset_class=UserActivityFilterSet)
    activity = graphene.relay.Node.Field(UserActivityType)
    me = graphene.Field(UserType)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        """Authenticated user resolver."""
        return info.find_context.user
