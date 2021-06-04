import graphene
import graphene_django


class SignInInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)




