import graphene
from users.types import UserType

#
# class UserOutput(UserType):
#
#     class Meta(UserType.Meta):
#         name = 'UserOutput'


class AuthenticationOutput(graphene.ObjectType):

    class Meta:
        name = 'Authentication'

    access_token = graphene.String(name='accessToken')
    refresh_token = graphene.String(name='refreshToken')
    me = graphene.Field(UserType)


class SignOutOutput(graphene.ObjectType):
    class Meta:
        name = 'Message'

    message = graphene.String()


class PresignField(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()


class PresignAWSImageUploadOutput(graphene.ObjectType):

    class Meta:
        name = 'Presign'

    fields = graphene.List(PresignField)
    url = graphene.String()




