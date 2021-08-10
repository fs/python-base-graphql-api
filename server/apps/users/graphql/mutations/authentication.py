import graphene
from django.contrib.auth import authenticate, get_user_model
from server.apps.users.graphql import inputs, outputs
from server.apps.users.models import UserActivity
from server.apps.users.signals import user_activity_signal
from server.core.auth.jwt import mixins
from server.core.auth.jwt.decorators import login_required
from server.core.auth.jwt.exceptions import InvalidCredentials

User = get_user_model()


class SignIn(mixins.ObtainPairMixin, graphene.Mutation):
    """JWT signin mutation for users."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input_ = inputs.SignInInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
        user = authenticate(info.context, **input_)
        if not user:
            raise InvalidCredentials()

        tokens = cls.generate_pair(user)
        user_activity_signal.send(cls, user=user, activity=UserActivity.USER_LOGGED_IN)
        return cls.Output(me=user, **tokens)


class SignUp(mixins.ObtainPairMixin, graphene.Mutation):
    """Signup mutation with JWT tokens."""

    Output = outputs.AuthenticationOutput

    class Arguments:
        input_ = inputs.SignUpInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
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
        tokens = cls.update_pair(info.context)
        return cls.Output(me=info.context.user, **tokens)


class SignOut(mixins.RevokeTokenMixin, graphene.Mutation):
    """Refresh tokens revoking mutation."""

    Output = outputs.SignOutOutput

    class Arguments:
        input_ = inputs.SignOutInput(required=True, name='input')

    @classmethod
    def mutate(cls, _, info, input_):
        context = info.context
        everywhere = input_.get('everywhere', False)

        if context.user.is_authenticated:
            cls.logout(info.context, everywhere)

        return cls.Output(message='Success')
