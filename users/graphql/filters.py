import django_filters

from users.models import UserActivity


class UserActivityFilterSet(django_filters.FilterSet):
    events = django_filters.MultipleChoiceFilter(choices=UserActivity.EVENT_CHOICES, field_name='event')

    class Meta:
        model = UserActivity
        fields = ['events']
