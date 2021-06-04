import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    avatarUrl = graphene.String(source='avatar')
    firstName = graphene.String(source='first_name')
    lastName = graphene.String(source='last_name')

    class Meta:
        model = User
        name = 'User'
        fields = ('id', 'email')

