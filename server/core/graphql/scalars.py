import graphene
from django.forms import ValidationError as DjangoValidationError
from server.apps.users.exceptions import ValidationError


class String(graphene.Scalar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = kwargs['validators']
        print('test')

    def validate_value(self, value):
        for validator in self.validators:
            try:
                validator(value)
            except DjangoValidationError:
                raise ValidationError('Invalid email')

        return value

    serialize = validate_value
    parse_value = validate_value
    parse_literal = validate_value
