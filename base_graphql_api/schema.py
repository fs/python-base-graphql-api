import graphene
import graphql_jwt
import users.graphql.query
import users.graphql.mutation
import users.jwt_authentication.mutations

from graphene_django.debug import DjangoDebug


class Query(
    users.graphql.query.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    users.jwt_authentication.mutations.Mutation
               ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
