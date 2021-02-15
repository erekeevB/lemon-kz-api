import graphene
import graphql_jwt
import re
from .types import *

class RegisterMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password1 = graphene.String()
        password2 = graphene.String()

    message = graphene.String()

    errors = graphene.List(graphene.String)

    def mutate(root, info, username, email, password1, password2):
        errors = []
        message = None
        regex = '^[a-z0-9]+[\._-]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if len(username) < 2:
            errors.append("Username length must be at least 2!")
        elif len(username) > 15:
            errors.append("Username length must be shorter than 15!")

        if len(email) < 1:
            errors.append("Email too short!")
        elif not (re.search(regex, email)):
            errors.append("Incorrect format for e-mail!")

        if len(password1) < 7:
            errors.append("Password length must be at least 8!")
        elif password1 != password2:
            errors.append("Passwords do not match!")

        if len(errors) != 0:
            return RegisterMutation(errors=errors, message = message)

        print(password1 + " " + password2)
        
        user = User.objects.create(username = username, email = email, password = password1)
        user.set_password(password1)
        user.save()

        message = "Successfully registered!"

        return RegisterMutation(errors = errors, message = message)

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)