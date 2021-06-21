import graphene
import users.graphql.mutations
import users.graphql.quyeries

from graphene_django.debug import DjangoDebug


class Query(
    graphene.ObjectType,
    users.graphql.quyeries.Query,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    users.graphql.mutations.Mutation
):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
