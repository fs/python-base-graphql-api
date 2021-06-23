import graphene
from django_filters.utils import get_model_field


def get_filtering_args_from_filterset(filterset_class, type):
    """ Inspect a FilterSet and produce the arguments to pass to
        a Graphene Field. These arguments will be available to
        filter against in the GraphQL
    """
    from graphene_django.forms.converter import convert_form_field

    args = {}
    model = filterset_class._meta.model
    for name, filter_field in filterset_class.base_filters.items():
        form_field = None
        filter_type = filter_field.lookup_expr

        if name in filterset_class.declared_filters:
            # Get the filter field from the explicitly declared filter
            form_field = filter_field.field
            field = convert_form_field(form_field)
        else:
            # Get the filter field with no explicit type declaration
            model_field = get_model_field(model, filter_field.field_name)
            if filter_type != "isnull" and hasattr(model_field, "formfield"):
                form_field = model_field.formfield(
                    required=filter_field.extra.get("required", False)
                )

            # Fallback to field defined on filter if we can't get it from the
            # model field
            if not form_field:
                form_field = filter_field.field

            field = convert_form_field(form_field)

        if filter_type in ["in", "range"]:
            # Replace CSV filters (`in`, `range`) argument type to be a list of
            # the same type as the field.  See comments in
            # `replace_csv_filters` method for more details.
            field = graphene.List(field.get_type())

        field_type = field.Argument()
        field_type.description = str(filter_field.label) if filter_field.label else None
        args[name] = field_type

    return args
