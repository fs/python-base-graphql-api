import graphene


class SignInInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UpdatePasswordInput(graphene.InputObjectType):
    password = graphene.String(required=True)
    reset_token = graphene.String(required=True, name='resetToken')


class ImageUploader(graphene.InputObjectType):
    id = graphene.String(required=True)
    storage = graphene.String(default='cache')


class UpdateUserInput(graphene.InputObjectType):
    email = graphene.String()
    first_name = graphene.String(name='firstName')
    last_name = graphene.String(name='lastName')
    current_password = graphene.String(name='currentPassword')
    password = graphene.String()
    # avatar = graphene.Field()
