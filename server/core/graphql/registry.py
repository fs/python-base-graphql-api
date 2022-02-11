
from graphene_django.registry import Registry


class FieldDescriptionDrivenRegistry(Registry):
    """Registry-class for registering fields with Django model description (verbose name)."""

    @staticmethod
    def set_graphene_field_description(field, converted):
        """Updates kwargs for description key from model field definition of graphql description is empty."""
        field_description = None
        graphene_field_description = converted.kwargs.get('description', None)
        if not graphene_field_description:
            field_description = field.verbose_name

        converted.kwargs.update({'description': field_description})

    def register_converted_field(self, field, converted):
        """Extended register of converted field to set additional options."""
        self.set_graphene_field_description(field, converted)
        super().register_converted_field(field, converted)
