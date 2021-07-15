import graphene
from users.graphql import inputs, outputs
from users.jwt_auth import mixins
from users.jwt_auth.decorators import login_required
from users.models import UserActivity
from users.signals import user_activity_signal


class UpdateUser(mixins.UpdateUserMixin, graphene.Mutation):
    """User fields updating mutation. Also saves user avatar image."""

    Output = outputs.UserType

    class Arguments:
        input_ = inputs.UpdateUserInput(required=True, name='input')

    @classmethod
    @login_required
    def mutate(cls, _, info, input_):
        context = info.context
        cls.update_user(context, input_)
        user_activity_signal.send(cls, user=context.user, activity=UserActivity.USER_UPDATED)
        return context.user


class PresignImagePresignUpload(mixins.ImagePresignMixin, graphene.Mutation):
    """AWS image direct upload. Generate headers and url for direct image upload from frontend."""

    Output = outputs.PresignAWSImageUploadOutput

    class Arguments:
        input_ = inputs.PresignAWSImageUploadInput(required=True, name='input')

    @classmethod
    @login_required
    def mutate(cls, _, info, input_):
        presign = cls.get_presign_upload(info.context.user, **input_)
        url = presign.get('url')
        fields = presign.get('fields')
        fields_out = [{'key': key, 'value': fields[key]} for key in fields]
        return cls.Output(url=url, fields=fields_out)


class RequestPasswordRecovery(mixins.PasswordRecoveryMixin, graphene.Mutation):
    """User password recovering process."""

    Output = outputs.PasswordRecoveryOutput

    class Arguments:
        input_ = inputs.PasswordRecoveryInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
        email = input_.get('email')
        user = cls.recovery(email)
        if user is not None:
            user_activity_signal.send(cls, user=user, activity=UserActivity.RESET_PASSWORD_REQUESTED)

        return cls.Output()


class UpdatePassword(mixins.ObtainPairMixin, mixins.UpdatePasswordMixin, graphene.Mutation):
    """User password recovering by reset token."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input_ = inputs.UpdatePasswordInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
        user = cls.update_password(**input_)
        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_RESET_PASSWORD)
        return cls.Output(me=user, **tokens)
