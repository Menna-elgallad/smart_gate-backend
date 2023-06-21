import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ext import db
from models.gate_model import Gate as GateModel
from flask_graphql_auth import mutation_header_jwt_required,query_header_jwt_required


class Gate(SQLAlchemyObjectType):
    class Meta:
        model = GateModel


class GatesQuery():
    gates = graphene.List(Gate)
    gate = graphene.Field(Gate, gateId=graphene.String())

    @query_header_jwt_required
    def resolve_gates(self, info):
        return GateModel.get_all()
    
    @query_header_jwt_required
    def resolve_gate(self, info, gateId):
        return GateModel.query.filter_by(id=gateId).first()
    


class CreateGate(graphene.Mutation):

    gate = graphene.Field(Gate)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        lat = graphene.String(required=True)
        long = graphene.String(required=True)
        
    @mutation_header_jwt_required
    def mutate(self, info, name, description, lat, long):
        oldGate = GateModel.query.filter_by(name=name).first()
        if oldGate : raise Exception('name should be unique')
        gateInfo = GateModel(name, description, lat, long)
        db.session.add(gateInfo)
        db.session.commit()
        return CreateGate(gate=gateInfo)
