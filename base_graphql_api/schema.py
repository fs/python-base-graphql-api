import graphene
import users.mutations

from graphene_django.debug import DjangoDebug


class Query(
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    users.mutations.Mutation
               ):
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
