import graphene
from django.contrib.auth import authenticate, get_user_model
from users.graphql import inputs, outputs
from users.jwt_auth import mixins
from users.jwt_auth.decorators import login_required
from users.jwt_auth.exceptions import InvalidCredentials
from users.models import UserActivity
from users.signals import user_activity_signal

User = get_user_model()


class SignIn(mixins.ObtainPairMixin, graphene.Mutation):
    """JWT signin mutation for users."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.SignInInput(required=True)

    @classmethod
    def mutate(cls, _, info, input_):
        user = authenticate(info.find_context, **input_)
        if not user:
            raise InvalidCredentials()

        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_LOGGED_IN)
        return cls.Output(me=user, **tokens)


class SignUp(mixins.ObtainPairMixin, graphene.Mutation):
    """Signup mutation with JWT tokens."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.SignUpInput(required=True)

    @classmethod
    def mutate(cls, _, __, input_):
        user = User.objects.create_user(**input_)
        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_REGISTERED)
        return cls.Output(me=user, **tokens)


class UpdateTokenPair(mixins.UpdateTokenPairMixin, graphene.Mutation):
    """JWT tokens updating mutation."""

    Output = outputs.AuthenticationOutput

    @classmethod
    @login_required
    def mutate(cls, _, info):
        tokens = cls.update_pair(info.find_context)
        return cls.Output(me=info.find_context.user, **tokens)


class SignOut(mixins.RevokeTokenMixin, graphene.Mutation):
    """Refresh tokens revoking mutation."""

    Output = outputs.SignOutOutput

    class Arguments:
        input = inputs.SignOutInput(required=True)

    @classmethod
    def mutate(cls, _, info, input_):
        context = info.find_context
        everywhere = input_.get('everywhere', False)

        if context.user.is_authenticated:
            cls.logout(info.find_context, everywhere)

        return cls.Output(message='Success')


class UpdateUser(mixins.UpdateUserMixin, graphene.Mutation):
    """User fields updating mutation. Also saves user avatar image."""

    Output = outputs.UserType

    class Arguments:
        input = inputs.UpdateUserInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input_):
        context = info.find_context
        cls.update_user(context, input_)
        user_activity_signal.send(cls, user=context.user, activity=UserActivity.USER_UPDATED)
        return context.user


class PresignImagePresignUpload(mixins.ImagePresignMixin, graphene.Mutation):
    """AWS image direct upload. Generate headers and url for direct image upload from frontend."""

    Output = outputs.PresignAWSImageUploadOutput

    class Arguments:
        input = inputs.PresignAWSImageUploadInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input_):
        presign = cls.get_presign_upload(info.find_context.user, **input_)
        url = presign.get('url')
        fields = presign.get('fields')
        fields_out = [{'key': key, 'value': fields[key]} for key in fields]
        return cls.Output(url=url, fields=fields_out)


class RequestPasswordRecovery(mixins.PasswordRecoveryMixin, graphene.Mutation):
    """User password recovering process."""

    Output = outputs.PasswordRecoveryOutput

    class Arguments:
        input = inputs.PasswordRecoveryInput(required=True)

    @classmethod
    @graphene.resolve_only_args
    def mutate(cls, _, input_):
        email = input_.get('email')
        user = cls.recovery(email)
        if user is not None:
            user_activity_signal.send(cls, user=user, activity=UserActivity.RESET_PASSWORD_REQUESTED)

        return cls.Output()


class UpdatePassword(mixins.ObtainPairMixin, mixins.UpdatePasswordMixin, graphene.Mutation):
    """User password recovering by reset token."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.UpdatePasswordInput(required=True)

    @classmethod
    @graphene.resolve_only_args
    def mutate(cls, _, input_):
        user = cls.update_password(**input_)
        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_RESET_PASSWORD)
        return cls.Output(me=user, **tokens)


class Mutation:
    """Main users mutation."""

    sign_in = SignIn.Field(name='signin')
    sign_up = SignUp.Field(name='signup')
    sign_out = SignOut.Field(name='signout')
    update_tokens = UpdateTokenPair.Field(name='updateToken')
    update_user = UpdateUser.Field(name='updateUser')
    presign_image_upload = PresignImagePresignUpload.Field(name='presignData')
    request_password_recovery = RequestPasswordRecovery.Field(name='requestPasswordRecovery')
    update_password = UpdatePassword.Field(name='updatePassword')
