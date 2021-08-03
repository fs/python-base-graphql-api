import graphene
from server.apps.users.graphql.filters import UserActivityFilterSet
from server.apps.users.graphql.types import UserActivityType, UserType
from server.core.auth.jwt.decorators import login_required
from server.core.graphql.fields.connection_fields import FilterConnectionField


class Query(object):
    """Users main GraphQL Query."""

    activities = FilterConnectionField(UserActivityType, filterset_class=UserActivityFilterSet)
    activity = graphene.relay.Node.Field(UserActivityType)
    me = graphene.Field(UserType)

    @classmethod
    @login_required
    def resolve_me(cls, _, info):
        """Authenticated user resolver."""
        return info.context.user
