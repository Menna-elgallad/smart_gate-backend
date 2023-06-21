import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from ext import db
from models.user_model import User as UserModel
from flask_graphql_auth import (
    get_jwt_identity,
    create_access_token,
    query_header_jwt_required
)


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('password')


class UserQuery():
    me = graphene.Field(User)

    @classmethod
    @query_header_jwt_required
    def resolve_me(cls, info, *args):
        username = get_jwt_identity()
        return UserModel.query.filter_by(username=username).first()


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        fcmToken = graphene.String(required=False)
        password = graphene.String()

    access_token = graphene.String()
    user = graphene.Field(lambda: User)

    def mutate(self, info, **kwargs):
        user = None
        if not kwargs:
            raise Exception('Must provide username/email and password')
        if kwargs.get('username'):
            user = UserModel.query.filter_by(
                username=kwargs['username']).first()
        else:
            user = UserModel.query.filter_by(email=kwargs['email']).first()

        if not user:
            raise Exception('user not found')
        decrepted_password = UserModel.verify_password(
            user, kwargs['password'])
        if decrepted_password:
            print(kwargs)
            if 'fcmToken' in kwargs:
                tokens = user.fcm_tokens or []
                tokens.append(kwargs['fcmToken'])
                db.session.query(UserModel).filter_by(
                    username=user.username).update({'fcm_tokens': tokens})
                db.session.commit()
            return Login(access_token=create_access_token(user.username), user=user)
        else:
            raise Exception('wrong credentials')


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, username, password, email, name):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise Exception('User already exists')
        user = UserModel(username=username, name=name,
                         password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)
