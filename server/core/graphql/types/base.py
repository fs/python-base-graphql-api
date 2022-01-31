
import warnings
from copy import deepcopy
from typing import Any, Dict, List, Type

from graphene import Field
from graphene.relay import Connection, Node
from graphene.types.interface import Interface
from graphene.types.objecttype import ObjectType
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.registry import Registry
from graphene_django.types import (
    ALL_FIELDS,
    DJANGO_FILTER_INSTALLED,
    DjangoObjectType,
    DjangoObjectTypeOptions,
    construct_fields,
    get_global_registry,
    validate_fields,
)
from graphene_django.utils import is_valid_django_model
from server.core.graphql.registry import FieldDescriptionDrivenRegistry


class PatchedDjangoObjectTypeOptions(DjangoObjectTypeOptions):
    """Redefined class for adding special attributes for implementing interface fields."""

    possible_types = ()
    default_resolver = None


class DescriptionDrivenDjangoObjectType(DjangoObjectType):
    """
    Redefined class for adding possibility of getting field description and auto add it to schema.

    Class in general repeats DjangoObjectType, but adds defining of interface fields
    by him (not by parents) and adds merging django-field and interface-field params.
    """

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        registry=FieldDescriptionDrivenRegistry(),
        skip_registry=False,
        only_fields=None,  # deprecated in favour of `fields`
        fields=None,
        exclude_fields=None,  # deprecated in favour of `exclude`
        exclude=None,
        filter_fields=None,
        filterset_class=None,
        connection=None,
        connection_class=None,
        use_connection=None,
        interfaces=(),
        convert_choices_to_enum=True,
        _meta=None,
        **options,
    ):
        assert is_valid_django_model(model), (
            'You need to pass a valid Django Model in {}.Meta, received "{}".'
        ).format(cls.__name__, model)

        if not registry:
            registry = get_global_registry()

        assert isinstance(registry, Registry), (
            'The attribute registry in {} needs to be an instance of '
            'Registry, received "{}".'
        ).format(cls.__name__, registry)

        if filter_fields and filterset_class:
            raise Exception("Can't set both filter_fields and filterset_class")

        if not DJANGO_FILTER_INSTALLED and (filter_fields or filterset_class):
            raise Exception(
                (
                    "Can only set filter_fields or filterset_class if "
                    "Django-Filter is installed"
                ),
            )

        assert not (fields and exclude), (
            "Cannot set both 'fields' and 'exclude' options on "
            "DjangoObjectType {class_name}.".format(class_name=cls.__name__)
        )

        # Alias only_fields -> fields
        if only_fields and fields:
            raise Exception("Can't set both only_fields and fields")
        if only_fields:
            warnings.warn(
                "Defining `only_fields` is deprecated in favour of `fields`.",
                DeprecationWarning,
                stacklevel=2,
            )
            fields = only_fields
        if fields and fields != ALL_FIELDS and not isinstance(fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple or "__all__". '
                "Got %s." % type(fields).__name__,
            )

        # Alias exclude_fields -> exclude
        if exclude_fields and exclude:
            raise Exception("Can't set both exclude_fields and exclude")
        if exclude_fields:
            warnings.warn(
                "Defining `exclude_fields` is deprecated in favour of `exclude`.",
                DeprecationWarning,
                stacklevel=2,
            )
            exclude = exclude_fields
        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                "The `exclude` option must be a list or tuple. Got %s."
                % type(exclude).__name__,
            )

        if fields is None and exclude is None:
            warnings.warn(
                "Creating a DjangoObjectType without either the `fields` "
                "or the `exclude` option is deprecated. Add an explicit `fields "
                "= '__all__'` option on DjangoObjectType {class_name} to use all "
                "fields".format(class_name=cls.__name__),
                DeprecationWarning,
                stacklevel=2,
            )

        django_fields = yank_fields_from_attrs(
            construct_fields(model, registry, fields, exclude, convert_choices_to_enum),
            _as=Field,
        )

        if use_connection is None and interfaces:
            use_connection = any(
                (issubclass(interface, Node) for interface in interfaces),
            )

        if use_connection and not connection:
            # We create the connection automatically
            if not connection_class:
                connection_class = Connection

            connection = connection_class.create_type(
                "{}Connection".format(options.get("name") or cls.__name__),
                node=cls,
            )

        if connection is not None:
            assert issubclass(connection, Connection), (
                "The connection must be a Connection. Received {}"
            ).format(connection.__name__)

        if not _meta:
            _meta = PatchedDjangoObjectTypeOptions(cls)

        # Added in this class instead original DjangoObjectType:
        # Getting fields for django-model anf graphene model and merging them
        interface_fields = cls.get_interface_fields(interfaces)
        merged_fields = cls.merge_model_and_interface_fields(django_fields, interface_fields)

        _meta.model = model
        _meta.registry = registry
        _meta.filter_fields = filter_fields
        _meta.filterset_class = filterset_class
        _meta.fields = merged_fields
        _meta.connection = connection

        # Calling DjangoObjectType Parent with special interfaces as empty tuple
        super(ObjectType, cls).__init_subclass_with_meta__(  # noqa: WPS608
            _meta=_meta, interfaces=(), **options,
        )

        # Validate fields
        validate_fields(cls, model, _meta.fields, fields, exclude)

        if not skip_registry:
            registry.register(cls)

    @classmethod
    def get_interface_fields(cls, interfaces: List[Type[Interface]]) -> Dict[str, Any]:
        """Returns fields referred in list of interfaces."""
        fields = {}

        for interface in interfaces:
            assert issubclass(
                interface, Interface,
            ), f'All interfaces of {cls.__name__} must be a subclass of Interface. Received "{interface}".'

            fields.update(interface._meta.fields)

        for base in reversed(cls.__mro__):
            fields.update(yank_fields_from_attrs(base.__dict__, _as=Field))

        return fields

    @classmethod
    def merge_model_and_interface_fields(cls, django_fields, interface_fields) -> Dict[str, Any]:
        """
        Returns merged fields with solved conflicts in field description.

        For example, when Interface filed has got own field description and Django Models's Field has got own.
        Method will return redefined in Interface field's description.
        """
        merged_fields = deepcopy(django_fields)

        for field_name, field_description in interface_fields.items():
            # replace description from interface if it is not none.
            if field_description.description:
                merged_fields.get(field_name).description = field_description.description

        return merged_fields

    class Meta:
        abstract = True
