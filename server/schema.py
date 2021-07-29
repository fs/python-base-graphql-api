import graphene
import server.apps.users.graphql.mutations
import server.apps.users.graphql.mutations.mutation
import server.apps.users.graphql.resolvers
from graphene_django.debug import DjangoDebug


class Query(
    graphene.ObjectType,
    server.apps.users.graphql.resolvers.Query,
):
    """Main query for schema."""

    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    server.apps.users.graphql.mutations.mutation.Mutation,
):
    """Main mutation for schema."""

    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
