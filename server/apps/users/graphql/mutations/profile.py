import graphene
from server.apps.users import mixins as users_mixins
from server.apps.users.graphql import inputs, outputs
from server.apps.users.models import UserActivity
from server.apps.users.signals import user_activity_signal
from server.core.auth.jwt import mixins as jwt_mixins
from server.core.auth.jwt.decorators import login_required


class UpdateUser(users_mixins.UpdateUserMixin, graphene.Mutation):
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


class PresignImagePresignUpload(users_mixins.ImagePresignMixin, graphene.Mutation):
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


class RequestPasswordRecovery(users_mixins.PasswordRecoveryMixin, graphene.Mutation):
    """User password recovering process."""

    Output = outputs.PasswordRecoveryOutput

    class Arguments:
        input_ = inputs.PasswordRecoveryInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
        email = input_.get('email')
        reset_token = cls.recovery(email)
        if reset_token is not None:
            user_activity_signal.send(cls, user=reset_token.user, activity=UserActivity.RESET_PASSWORD_REQUESTED)

        return cls.Output()


class UpdatePassword(jwt_mixins.ObtainPairMixin, users_mixins.UpdatePasswordMixin, graphene.Mutation):
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
