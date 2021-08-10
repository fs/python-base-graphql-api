import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from server.apps.users.models import UserActivity
from server.core.auth.jwt.decorators import login_required

User = get_user_model()


class UserType(DjangoObjectType):
    """GraphQL type based on user model."""

    avatar = graphene.String(name='avatarUrl')
    last_name = graphene.String(name='lastName')
    first_name = graphene.String(name='firstName')

    class Meta:
        model = User
        name = 'User'
        fields = ('id', 'email')
        interfaces = (graphene.relay.Node, )

    def resolve_avatar(self, _):
        """User avatar url resolving."""
        return self.avatar.url if self.avatar else None


class UserActivityType(DjangoObjectType):
    """GraphQL type based on UserActivity model."""

    title = graphene.String()
    created_at = graphene.String(name='createdAt')
    body = graphene.String()
    user = graphene.Field(UserType)

    class Meta:
        model = UserActivity
        name = 'Activity'
        fields = ('id', 'event')
        interfaces = (graphene.relay.Node, )

    def resolve_title(self, _):
        """Resolve event choices display name."""
        return self.get_event_display()

    # TODO: make body
    def resolve_body(self, info):
        """Resolve event description."""
        return 'TEST'

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        """Method for wrap user activity data in login_required decorator."""
        return queryset
