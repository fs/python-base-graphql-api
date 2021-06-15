import graphene


class SignInInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class SignOutInput(graphene.InputObjectType):
    everywhere = graphene.Boolean()


class SignUpInput(graphene.InputObjectType):
    email = graphene.String()
    first_name = graphene.String(name='firstName')
    last_name = graphene.String(name='lastName')
    password = graphene.String()
    # avatar = graphene.Field()


class UpdatePasswordInput(graphene.InputObjectType):
    password = graphene.String(required=True)
    reset_token = graphene.String(required=True, name='resetToken')


class ImageUploaderMetadata(graphene.InputObjectType):
    size = graphene.Int(required=True)
    filename = graphene.String(required=True)
    mime_type = graphene.String(required=True, name='mimeType')


class ImageUploader(graphene.InputObjectType):
    id = graphene.String(required=True)
    storage = graphene.String(default='cache')
    metadata = graphene.Field(ImageUploaderMetadata)


class UpdateUserInput(SignUpInput):
    current_password = graphene.String(name='currentPassword')
    avatar = graphene.Field(ImageUploader)


class PresignAWSImageUploadInput(graphene.InputObjectType):
    filename = graphene.String(required=True)
    file_type = graphene.String(required=True, name='type')

    class Meta:
        name = 'PresignDataInput'

