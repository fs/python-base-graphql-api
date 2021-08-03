import graphene
from django import forms
from graphene_django.forms.converter import convert_form_field


@convert_form_field.register(forms.MultipleChoiceField)
def convert_form_field_to_string_list(field):
    """Overriding graphene_django django_filters field with choices converting."""
    enum = graphene.Enum(field.label, field.choices)
    return graphene.List(enum, required=field.required)
