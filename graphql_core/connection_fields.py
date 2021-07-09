from django.core.exceptions import ValidationError
from graphene.utils.str_converters import to_snake_case as parse_to_snake_case
from graphene_django.filter import DjangoFilterConnectionField


def define_enum_as_filter_field(key, args, filters):
    """Parse enum to filter."""
    for enum_value in args:
        filters[key] = enum_value.name if getattr(enum_value, 'name', None) else enum_value


def get_filter_kwargs(args, filtering_args):
    """Filter kwargs definition."""
    filters = {}
    for key, arg_value in args.items():
        if key in filtering_args:
            if key == 'order_by' and arg_value is not None:
                arg_value = parse_to_snake_case(arg_value)

            if isinstance(arg_value, list):
                # Added for list of enums field (graphene.List(graphene.Enum))
                # Without this line input enum values looks like '[ActivityEnum].[USER_LOGGED_IN]',
                # where ActivityEnum - name of class, USER_LOGGED_IN - choices value of model field
                define_enum_as_filter_field(key, args, filters)
            else:
                filters[key] = arg_value

    return filters


class FilterConnectionField(DjangoFilterConnectionField):
    """Override filter graphene_django connection field for enum as filter field."""

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):  # noqa: WPS211
        """Overriding filter kwargs definition."""
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(connection, iterable, info, args)  # noqa: WPS608
        filterset = filterset_class(data=get_filter_kwargs(args, filtering_args), queryset=qs, request=info.context)

        if filterset.form.is_valid():
            return filterset.qs

        raise ValidationError(filterset.form.errors.as_json())
