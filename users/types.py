import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    avatar = graphene.String(name='avatarUrl')
    last_name = graphene.String(name='lastName')
    first_name = graphene.String(name='firstName')

    class Meta:
        model = User
        name = 'User'
        fields = ('id', 'email')

    def resolve_avatar(self, info):
        return self.avatar.url

