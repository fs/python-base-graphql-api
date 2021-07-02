from django.core.exceptions import ValidationError
from graphene.utils.str_converters import to_snake_case
from graphene_django.filter import DjangoFilterConnectionField


class FilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        def filter_kwargs():
            kwargs = {}
            for k, v in args.items():
                if k in filtering_args:
                    if k == "order_by" and v is not None:
                        v = to_snake_case(v)

                    if isinstance(v, list):
                        # Added for list of enums field:
                        # Without this line input enum values looks like '[ActivityEnum].[USER_LOGGED_IN]',
                        # where ActivityEnum - name of class, USER_LOGGED_IN - choices value of model field
                        kwargs[k] = [item.name if getattr(item, 'name') else item for item in v]
                    else:
                        kwargs[k] = v

            return kwargs

        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filterset = filterset_class(
            data=filter_kwargs(), queryset=qs, request=info.context
        )
        if filterset.form.is_valid():
            return filterset.qs
        raise ValidationError(filterset.form.errors.as_json())
