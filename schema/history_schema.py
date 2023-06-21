from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene
from models.history_model import History as HistoryModel
from flask_graphql_auth import mutation_header_jwt_required, query_header_jwt_required
from ext import db
from datetime import datetime
from schema.car_schema import Car
from models.car_model import Car as CarModel
from schema.gate_schema import Gate
from models.gate_model import Gate as GateModel

class History(SQLAlchemyObjectType):

    class Meta:
        model = HistoryModel
    car = graphene.Field(Car)
    gate = graphene.Field(Gate)
    def resolve_car(self, info):
        return CarModel.query.filter_by(id=self.car_id).first()
    def resolve_gate(self, info):
        return GateModel.query.filter_by(id=self.gate_id).first()

class HistoryQuery():
    history = graphene.List(History , gate_id=graphene.String() , car_id=graphene.String() , created=graphene.String())

    @query_header_jwt_required
    def resolve_history(self, info , **kwargs):
        return HistoryModel.query.filter_by(**kwargs)
    