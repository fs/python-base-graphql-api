import graphene
import users.graphql.mutations
import users.graphql.mutations.mutation
import users.graphql.resolvers
from graphene_django.debug import DjangoDebug


class Query(
    graphene.ObjectType,
    users.graphql.resolvers.Query,
):
    """Main query for schema."""

    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    users.graphql.mutations.mutation.Mutation,
):
    """Main mutation for schema."""

    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
