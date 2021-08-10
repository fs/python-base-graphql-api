import graphene
import server.apps.users.graphql.mutations
import server.apps.users.graphql.mutations.mutation
import server.apps.users.graphql.resolvers
import strawberry


@strawberry.type
class Query(
    graphene.ObjectType,
    server.apps.users.graphql.resolvers.Query,
):
    """Main query for schema."""


@strawberry.type
class Mutation(
    graphene.ObjectType,
    server.apps.users.graphql.mutations.mutation.Mutation,
):
    """Main mutation for schema."""


schema = strawberry.Schema(query=Query, mutation=Mutation)
