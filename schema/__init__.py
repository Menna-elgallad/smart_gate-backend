import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from schema.user_schema import UserQuery
from schema.user_schema import Login, CreateUser
from schema.gate_schema import GatesQuery, CreateGate
from schema.camera_schema import CameraQuery, AddCamera
from schema.car_schema import CarQuery,AddCar,BlockCar,UnBlockCar,ValidateCar
from schema.history_schema import HistoryQuery
from schema.notification_schema import NotificationQuery

class Query(graphene.ObjectType, UserQuery, GatesQuery, CameraQuery,CarQuery , HistoryQuery,NotificationQuery):
    class Meta:
        pass


class Mutations(graphene.ObjectType):
    login = Login.Field()
    register = CreateUser.Field()
    createGate = CreateGate.Field()
    addCamera = AddCamera.Field()
    addCar = AddCar.Field()
    blockCar = BlockCar.Field()
    unblockCar=UnBlockCar.Field()
    validateCar=ValidateCar.Field()
schema = graphene.Schema(query=Query, mutation=Mutations)
