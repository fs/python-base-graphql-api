import graphene
from server.apps.users.graphql.types import UserType


class AuthenticationOutput(graphene.ObjectType):
    """Output for authenticated mutation."""

    class Meta:
        name = 'Authentication'

    access_token = graphene.String(name='accessToken')
    refresh_token = graphene.String(name='refreshToken')
    me = graphene.Field(UserType)


class SignOutOutput(graphene.ObjectType):
    """Output message after signout."""

    class Meta:
        name = 'Message'

    message = graphene.String()


class PasswordRecoveryOutput(graphene.ObjectType):
    """Output with default messages after password recovery request."""

    class Meta:
        name = 'DetailedMessage'

    message = graphene.String(default_value='Instructions sent')
    detail = graphene.String(default_value='Password recovery instructions were sent if that account exists')


class PresignField(graphene.ObjectType):
    """Output for AWS authenticated headers in key, value view."""

    key = graphene.String()
    value = graphene.String()  # noqa: WPS110


class PresignAWSImageUploadOutput(graphene.ObjectType):
    """Output for AWS direct upload options with authenticated headers and url."""

    class Meta:
        name = 'Presign'

    fields = graphene.List(PresignField)
    url = graphene.String()
