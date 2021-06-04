import graphene
import graphql_jwt
import users.graphql.query
import users.graphql.mutation

from graphene_django.debug import DjangoDebug


class Query(
    users.graphql.query.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    users.graphql.mutation.Mutation
               ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
