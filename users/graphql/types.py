import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoListObjectType, PageGraphqlPagination


from users.models import UserActivity

User = get_user_model()


class UserType(DjangoObjectType):
    avatar = graphene.String(name='avatarUrl')
    last_name = graphene.String(name='lastName')
    first_name = graphene.String(name='firstName')

    class Meta:
        model = User
        name = 'User'
        fields = ('id', 'email')
        interfaces = (graphene.relay.Node, )

    def resolve_avatar(self, info):
        return self.avatar.url


class UserActivityType(DjangoObjectType):
    title = graphene.String()
    created_at = graphene.String(name='createdAt')
    body = graphene.String()
    user = graphene.Field(UserType)

    class Meta:
        model = UserActivity
        name = 'Activity'
        fields = ('id', 'event')
        interfaces = (graphene.relay.Node, )
        filter_fields = ['event']

    def resolve_title(self, _):
        return self.get_event_display()

    def resolve_body(self, info):
        return 'TEST'


