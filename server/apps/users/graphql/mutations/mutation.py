from server.apps.users.graphql.mutations import authentication, profile


class Mutation:
    """Main users mutation."""

    sign_in = authentication.SignIn.Field(name='signin')
    sign_up = authentication.SignUp.Field(name='signup')
    sign_out = authentication.SignOut.Field(name='signout')
    update_tokens = authentication.UpdateTokenPair.Field(name='updateToken')
    update_user = profile.UpdateUser.Field(name='updateUser')
    presign_image_upload = profile.PresignImagePresignUpload.Field(name='presignData')
    request_password_recovery = profile.RequestPasswordRecovery.Field(name='requestPasswordRecovery')
    update_password = profile.UpdatePassword.Field(name='updatePassword')
