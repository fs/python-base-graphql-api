import django_filters
from server.apps.users.models import UserActivity


class UserActivityFilterSet(django_filters.FilterSet):
    """Filterset for user activity mutation."""

    events = django_filters.MultipleChoiceFilter(choices=UserActivity.EVENT_CHOICES, field_name='event')

    class Meta:
        model = UserActivity
        fields = ['events']
