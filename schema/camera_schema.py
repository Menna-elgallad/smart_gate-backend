from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene
from models.camera_model import Camera as CameraModel
from flask_graphql_auth import mutation_header_jwt_required, query_header_jwt_required
from ext import db

class Camera(SQLAlchemyObjectType):
    class Meta:
        model = CameraModel


class CameraQuery():
    allCamera = graphene.List(Camera)
    gateCameras = graphene.List(Camera, gateId=graphene.String())
    camera = graphene.Field(Camera, cameraId=graphene.String())

    @query_header_jwt_required
    def resolve_allCamera(self, info):
        return CameraModel.get_all()

    @query_header_jwt_required
    def resolve_gateCameras(self, info, gateId):
        return CameraModel.query.filter_by(gate_id=gateId)
    
    @query_header_jwt_required
    def resolve_camera(self, info, cameraId):
        return CameraModel.query.filter_by(id=cameraId).first()
    


class AddCamera(graphene.Mutation):
    camera = graphene.Field(Camera)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String(required=True)
        api_url = graphene.String(required=True)
        gate_id = graphene.String(required=True)

    @mutation_header_jwt_required
    def mutate(self, info, name, description, url, api_url , gate_id):
        oldGate = CameraModel.query.filter_by(name=name).first()
        if oldGate:
            raise Exception('name should be unique')
        cameraInfo = CameraModel(name, description, url, api_url , gate_id)
        db.session.add(cameraInfo)
        db.session.commit()
        return AddCamera(camera=cameraInfo)
