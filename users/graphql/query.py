import graphene
from django.contrib.auth import get_user_model
from .types import UserType

User = get_user_model()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all = graphene.List(UserType)

    @staticmethod
    def resolve_all(_, info):
        return User.objects.all()

    @staticmethod
    def resolve_me(info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not authorized')

        return user
