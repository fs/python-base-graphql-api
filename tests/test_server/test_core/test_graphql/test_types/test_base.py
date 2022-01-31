
import graphene
from django.db import models
from django.test.testcases import TestCase
from graphene_django import DjangoObjectType
from server.core.graphql.types.base import DescriptionDrivenDjangoObjectType
from tests.test_server.test_core.test_graphql.models import Person


class TestDescriptionDrivenDjangoObjectType(TestCase):
    """Tests for checking filling description from Django model, interface, and ObjectType."""

    @staticmethod
    def get_model_field_info(model: models.Model, field_name: str) -> models.Field:
        """Returns Field object from given model by field's name."""
        return model._meta.get_field(field_name)   # noqa: WPS437

    @staticmethod
    def get_schema_field_info(schema: graphene.Schema, field_name: str):
        """Returns schema's Field object from given schema by field's name."""
        return schema.graphql_schema.query_type.fields[field_name]

    def test_no_built_in_description_from_field(self):
        """Check no description from model's field using Type with DjangoObjectType."""
        class PersonType(DjangoObjectType):  # noqa: WPS431
            class Meta:
                model = Person
                fields = '__all__'

        schema = graphene.Schema(query=PersonType)

        model_field_description = self.get_model_field_info(Person, 'name').verbose_name

        self.assertNotEqual(
            self.get_schema_field_info(schema, 'name').description,
            model_field_description,
        )

    def test_get_description_from_field(self):
        """Check description field correctly fills from field's verbose_name."""
        class PersonType(DescriptionDrivenDjangoObjectType):  # noqa: WPS431
            class Meta:
                model = Person
                fields = '__all__'

        schema = graphene.Schema(query=PersonType)

        model_field_description = self.get_model_field_info(Person, 'name').verbose_name

        self.assertEqual(
            self.get_schema_field_info(schema, 'name').description,
            model_field_description,
        )

    def test_get_description_from_field_with_interface(self):  # noqa: WPS118, WPS210
        """Check description field correctly fills from field's interface if interface description is not null."""

        class PersonInterface(graphene.Interface):  # noqa: WPS431
            """Redefined person's name."""

            name = graphene.String(description='Interface person name description')

            @classmethod
            def resolve_name(cls, info, **kwargs):
                return 'awesome name'

        class PersonType(DescriptionDrivenDjangoObjectType):  # noqa: WPS431
            class Meta:
                model = Person
                fields = '__all__'
                interfaces = (PersonInterface,)

        schema = graphene.Schema(query=PersonType)

        model_field_description = self.get_model_field_info(Person, 'name').verbose_name
        self.assertNotEqual(
            self.get_schema_field_info(schema, 'name').description,
            model_field_description,
        )

    def test_get_description_from_field_with_interface_description_empty(self):  # noqa: WPS118, WPS210
        """Check description field fills from model even with interface when interface description is empty."""

        class PersonInterface(graphene.Interface):  # noqa: WPS431
            """Redefined person's name."""

            name = graphene.String()

            @classmethod
            def resolve_name(cls, info, **kwargs):
                return 'awesome name'

        class PersonType(DescriptionDrivenDjangoObjectType):  # noqa: WPS431
            class Meta:
                model = Person
                fields = '__all__'
                interfaces = (PersonInterface,)

        schema = graphene.Schema(query=PersonType)

        model_field_description = self.get_model_field_info(Person, 'name').verbose_name
        self.assertEqual(
            self.get_schema_field_info(schema, 'name').description,
            model_field_description,
        )

        interface_field_description = PersonInterface.name.kwargs.get('description', '')
        self.assertNotEqual(
            self.get_schema_field_info(schema, 'name').description,
            interface_field_description,
        )
