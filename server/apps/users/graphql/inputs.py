import strawberry


@strawberry.input
class SignInInput:
    """Signin mutation input."""

    email:  str
    password: str

@strawberry.input
class SignOutInput:
    """Signout mutation input, which revokes all user refresh tokens or current."""

    everywhere: bool

@strawberry.input
class SignUpInput:
    """Signup mutation input."""

    email: str
    first_name: str
    last_name: str
    password: str

@strawberry.input
class ImageUploaderMetadata:
    """AWS image metadata after direct uploading."""

    size: int
    filename: str
    mime_type: str

class ImageUploader:
    """AWS image data after direct uploading."""

    id: str
    storage: str
    metadata: ImageUploaderMetadata


class UpdateUserInput:
    """Updating user input fields with AWS image uploading."""

    current_password: str
    avatar: ImageUploader


class PresignAWSImageUploadInput:
    """AWS image info for direct upload headers generation."""

    filename: str
    file_type: str

    class Meta:
        name = 'PresignDataInput'


class PasswordRecoveryInput:
    """Input for user recovery request with email to which the recovery url will be sent."""

    email: str

    class Meta:
        name = 'RequestPasswordRecoveryInput'


class UpdatePasswordInput:
    """Input for password updating by reset token."""

    password: str
    reset_token: str

    class Meta:
        name = 'UpdatePasswordInput'
