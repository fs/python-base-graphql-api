import django_filters
from server.apps.users.models import UserActivity


class UserActivityFilterSet(django_filters.FilterSet):
    """Filterset for user activity mutation."""

    events = django_filters.MultipleChoiceFilter(
        choices=UserActivity.EVENT_CHOICES,
        field_name='event',
        label='ActivityEvent',  # label used in graphene field converter for enum name in core/graphql/field_converter.
    )

    class Meta:
        model = UserActivity
        fields = ['events']
