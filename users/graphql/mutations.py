import graphene
from django.contrib.auth import authenticate, get_user_model

from users.graphql import outputs, inputs
from users.jwt_authentication import mixins
from users.jwt_authentication.decorators import login_required
from users.jwt_authentication.exceptions import InvalidCredentials
from users.models import UserActivity
from users.signals import user_activity_signal

User = get_user_model()


class SignIn(mixins.ObtainPairMixin, graphene.Mutation):
    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.SignInInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        user = authenticate(info.context, **input)
        if not user:
            raise InvalidCredentials()

        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_LOGGED_IN)
        return cls.Output(me=user, **tokens)


class SignUp(mixins.ObtainPairMixin, graphene.Mutation):
    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.SignUpInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        user = User.objects.create_user(**input)
        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_REGISTERED)
        return cls.Output(me=user, **tokens)


class UpdateTokenPair(mixins.UpdateTokenPairMixin, graphene.Mutation):
    Output = outputs.AuthenticationOutput

    @classmethod
    @login_required
    def mutate(cls, _, info):
        tokens = cls.update_pair(info.context)
        return cls.Output(me=info.context.user, **tokens)


class SignOut(mixins.RevokeTokenMixin, graphene.Mutation):
    Output = outputs.SignOutOutput

    class Arguments:
        input = inputs.SignOutInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        everywhere = input.get('everywhere', False)
        cls.logout(info.context, everywhere)
        return cls.Output(message='Success')


class UpdateUser(mixins.UpdateUserMixin, graphene.Mutation):
    Output = outputs.UserType

    class Arguments:
        input = inputs.UpdateUserInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input):
        context = info.context
        cls.update_user(context, input)
        user_activity_signal.send(cls, user=context.user, activity=UserActivity.USER_UPDATED)
        return context.user


class PresignImagePresignUpload(mixins.ImagePresignMixin, graphene.Mutation):
    Output = outputs.PresignAWSImageUploadOutput

    class Arguments:
        input = inputs.PresignAWSImageUploadInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input):
        presign = cls.get_presign_upload(info.context.user, **input)
        url = presign.get('url')
        fields = presign.get('fields')
        fields_out = [{"key": key, "value": fields[key]} for key in fields]
        return cls.Output(url=url, fields=fields_out)


class RequestPasswordRecovery(mixins.PasswordRecoveryMixin, graphene.Mutation):
    Output = outputs.PasswordRecoveryOutput

    class Arguments:
        input = inputs.PasswordRecoveryInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        email = input.get('email')
        cls.recovery(email)
        user = User.objects.filter(email=email)
        if user.exists():
            user_activity_signal.send(cls, user=user[0], activity=UserActivity.RESET_PASSWORD_REQUESTED)

        return cls.Output()


class UpdatePassword(mixins.ObtainPairMixin, mixins.UpdatePasswordMixin, graphene.Mutation):
    Output = outputs.AuthenticationOutput

    class Arguments:
        input = inputs.UpdatePasswordInput(required=True)

    @classmethod
    def mutate(cls, _, __, input):
        user = cls.update_password(**input)
        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_RESET_PASSWORD)
        return cls.Output(me=user, **tokens)


class Mutation:
    sign_in = SignIn.Field(name='signin')
    sign_up = SignUp.Field(name='signup')
    sign_out = SignOut.Field(name='signout')
    update_tokens = UpdateTokenPair.Field(name='updateToken')
    update_user = UpdateUser.Field(name='updateUser')
    presign_image_upload = PresignImagePresignUpload.Field(name='presignData')
    request_password_recovery = RequestPasswordRecovery.Field(name='requestPasswordRecovery')
    update_password = UpdatePassword.Field(name='updatePassword')
