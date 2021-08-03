import graphene


class SignInInput(graphene.InputObjectType):
    """Sign in mutation input."""

    email = graphene.String(required=True)
    password = graphene.String(required=True)


class SignOutInput(graphene.InputObjectType):
    """Sign out mutation input, which revokes all user refresh tokens or current."""

    everywhere = graphene.Boolean()


class SignUpInput(graphene.InputObjectType):
    """Signup mutation input."""

    email = graphene.String()
    first_name = graphene.String(name='firstName')
    last_name = graphene.String(name='lastName')
    password = graphene.String()


class ImageUploaderMetadata(graphene.InputObjectType):
    """AWS image metadata after direct uploading."""

    size = graphene.Int(required=True)
    filename = graphene.String(required=True)
    mime_type = graphene.String(required=True, name='mimeType')


class ImageUploader(graphene.InputObjectType):
    """AWS image data after direct uploading."""

    id = graphene.String(required=True)
    storage = graphene.String()
    metadata = graphene.Field(ImageUploaderMetadata)


class UpdateUserInput(SignUpInput):
    """Updating user input fields with AWS image uploading."""

    current_password = graphene.String(name='currentPassword')
    avatar = graphene.Field(ImageUploader)


class PresignAWSImageUploadInput(graphene.InputObjectType):
    """AWS image info for direct upload headers generation."""

    filename = graphene.String(required=True)
    file_type = graphene.String(required=True, name='type')

    class Meta:
        name = 'PresignDataInput'


class PasswordRecoveryInput(graphene.InputObjectType):
    """Input for user recovery request with email to which the recovery url will be sent."""

    email = graphene.String(required=True)

    class Meta:
        name = 'RequestPasswordRecoveryInput'


class UpdatePasswordInput(graphene.InputObjectType):
    """Input for password updating by reset token."""

    password = graphene.String(required=True)
    reset_token = graphene.String(required=True, name='resetToken')

    class Meta:
        name = 'UpdatePasswordInput'
