from enum import Enum
from typing import Dict, List

from django.core.exceptions import ValidationError
from graphene.utils.str_converters import to_snake_case as parse_to_snake_case
from graphene_django.filter import DjangoFilterConnectionField


def get_enum_as_input(args: List) -> List[str]:
    """Parse enum to filter."""
    return [enum_value.name for enum_value in args]


def is_list_of_enums(args: List) -> bool:
    """Check list of enums containing."""
    if not args:
        return False
    return isinstance(args[0], Enum)


def define_filter_arg(field_name: str, field_value: object) -> object:
    """Filter field type definition."""
    if field_name == 'order_by' and field_value is not None:
        return parse_to_snake_case(field_value)
    elif isinstance(field_value, list) and field_value:
        if is_list_of_enums(field_value):
            # Added for list of enums field (graphene.List(graphene.Enum))
            # Without this line input enum values looks like '[ActivityEnum].[USER_LOGGED_IN]',
            # where ActivityEnum - name of class, USER_LOGGED_IN - choices value of model field
            return get_enum_as_input(field_value)
    return field_value


def get_filter_kwargs(all_args: List, filtering_args: List) -> Dict[str, str]:
    """Filter kwargs definition."""
    filters = {}
    for key, arg_value in all_args.items():
        if key not in filtering_args:
            break

        filters[key] = define_filter_arg(key, arg_value)

    return filters


class FilterConnectionField(DjangoFilterConnectionField):
    """Override filter graphene_django connection field for enum as filter field."""

    @classmethod
    def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):  # noqa: WPS211
        """Changed list filter field definition."""
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(connection, iterable, info, args)  # noqa: WPS608
        filterset = filterset_class(data=get_filter_kwargs(args, filtering_args), queryset=qs, request=info.context)

        if filterset.form.is_valid():
            return filterset.qs

        raise ValidationError(filterset.form.errors.as_json())
