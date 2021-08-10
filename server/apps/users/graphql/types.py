import strawberry
from django.contrib.auth import get_user_model
from server.apps.users.models import UserActivity
from server.core.auth.jwt.decorators import login_required
from strawberry.django import auto
from django.db.models import QuerySet

User = get_user_model()


@strawberry.django.type
class UserType:
    """GraphQL type based on user model."""

    id: auto
    avatar: auto
    last_name: auto
    first_name: auto

    class Meta:
        model = User
        name = 'User'
        fields = ('id', 'email')

    @strawberry.field
    def resolve_avatar(self):
        """User avatar url resolving."""
        return self.avatar.url if self.avatar else None


@strawberry.django.type
class UserActivityType:
    """GraphQL type based on UserActivity model."""

    id: auto
    title: auto
    created_at: auto
    body: auto
    user: UserType

    class Meta:
        model = UserActivity
        name = 'Activity'
        fields = ('id', 'event')

    @strawberry.field
    def resolve_title(self):
        """Resolve event choices display name."""
        return self.get_event_display()

    @strawberry.field
    # TODO: make body
    def resolve_body(self, info):
        """Resolve event description."""
        return 'TEST'

    @classmethod
    @login_required
    @strawberry.field
    def get_queryset(cls, queryset: QuerySet, info) -> QuerySet:
        """Method for wrap user activity data in login_required decorator."""
        return queryset
