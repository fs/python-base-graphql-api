import graphene

from django.contrib.auth import authenticate, get_user_model

from users.inputs import SignInInput, SignUpInput, SignOutInput, UpdateUserInput, PresignAWSImageUploadInput
from users.outputs import AuthenticationOutput, SignOutOutput, UserType, PresignAWSImageUploadOutput
from users.jwt_authentication.mixins import ObtainPairMixin, RevokeTokenMixin, UpdateTokenPairMixin, UpdateUserMixin, ImagePresignMixin
from users.jwt_authentication.decorators import login_required
from .jwt_authentication.exceptions import InvalidCredentials

User = get_user_model()


class SignIn(ObtainPairMixin, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignInInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        user = authenticate(info.context, **input)
        if not user:
            raise InvalidCredentials()

        tokens = cls.generate_pair(user)
        return cls.Output(me=user, **tokens)


class SignUp(ObtainPairMixin, graphene.Mutation):
    Output = AuthenticationOutput

    class Arguments:
        input = SignUpInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        user = User.objects.create_user(**input)
        tokens = cls.generate_pair(user)
        return cls.Output(me=user, **tokens)


class UpdateTokenPair(UpdateTokenPairMixin, graphene.Mutation):
    Output = AuthenticationOutput

    @classmethod
    @login_required
    def mutate(cls, _, info):
        tokens = cls.update_pair(info.context)
        return cls.Output(me=info.context.user, **tokens)


class SignOut(RevokeTokenMixin, graphene.Mutation):
    Output = SignOutOutput

    class Arguments:
        input = SignOutInput(required=True)

    @classmethod
    def mutate(cls, _, info, input):
        everywhere = input.get('everywhere', False)
        cls.logout(info.context, everywhere)
        return cls.Output(message='Success')


class UpdateUser(ImagePresignMixin, UpdateUserMixin, graphene.Mutation):
    Output = UserType

    class Arguments:
        input = UpdateUserInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input):
        cls.update_user(info.context, input)
        return info.context.user


class PresignImagePresignUpload(ImagePresignMixin, graphene.Mutation):
    Output = PresignAWSImageUploadOutput

    class Arguments:
        input = PresignAWSImageUploadInput(required=True)

    @classmethod
    @login_required
    def mutate(cls, _, info, input):
        presign = cls.get_presign_upload(info.context.user, **input)
        url = presign.get('url')
        fields = presign.get('fields')
        fields_out = []

        for key in fields:
            fields_out.append({"key": key, "value": fields[key]})

        return cls.Output(url=url, fields=fields_out)


class Mutation:
    sign_in = SignIn.Field(name='signin')
    sign_up = SignUp.Field(name='signup')
    sign_out = SignOut.Field(name='signout')
    update_tokens = UpdateTokenPair.Field(name='updateToken')
    update_user = UpdateUser.Field(name='updateUser')
    presign_image_upload = PresignImagePresignUpload.Field(name='presignData')


