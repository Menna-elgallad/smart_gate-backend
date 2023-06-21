import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ext import db
from models.notification_model import Notification as NotificationModel
from flask_graphql_auth import mutation_header_jwt_required,query_header_jwt_required

class Notification(SQLAlchemyObjectType):
    class Meta:
        model = NotificationModel
      

class NotificationQuery():
    notifications = graphene.List(Notification)
    notification = graphene.Field(Notification, notificationId=graphene.String())

    @query_header_jwt_required
    def resolve_notifications(self, info):
        return NotificationModel.get_all()
    
    @query_header_jwt_required
    def resolve_notification(self, info, notificationId):
        return NotificationModel.query.filter_by(id=notificationId).first()  