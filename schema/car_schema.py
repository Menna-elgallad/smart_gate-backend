from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene
from models.car_model import Car as CarModel
from flask_graphql_auth import mutation_header_jwt_required, query_header_jwt_required
from ext import db
from datetime import datetime
from models.history_model import History as HistoryModel
from models.gate_model import Gate as GateModel
import uuid
from utils.notifier import send_notification


class Car(SQLAlchemyObjectType):
    class Meta:
        model = CarModel


class CarQuery():
    allCars = graphene.List(Car)
    gateCars = graphene.List(Car, gateId=graphene.String())
    blockedCars = graphene.List(Car)
    car = graphene.Field(Car, carId=graphene.String())

    @query_header_jwt_required
    def resolve_allCars(self, info):
        return CarModel.get_all()

    @query_header_jwt_required
    def resolve_gateCars(self, info, gateId):
        allCars = CarModel.get_all()
        cars = [car for car in allCars if uuid.UUID(gateId) in car.gate_ids]
        return cars

    @query_header_jwt_required
    def resolve_blockedCars(self, info):
        return CarModel.query.filter_by(blocked=True)

    @query_header_jwt_required
    def resolve_car(self, info, carId):
        return CarModel.query.filter_by(id=carId).first()


class AddCar(graphene.Mutation):
    car = graphene.Field(Car)

    class Arguments:
        owner_name = graphene.String(required=True)
        plate_number = graphene.String(required=True)
        gate_ids = graphene.List(required=False, of_type=graphene.String)
        all_gates = graphene.Boolean(required=False)
        color = graphene.String(required=False)

    @mutation_header_jwt_required
    def mutate(self, info, owner_name, plate_number, color, gate_ids=[], all_gates=False):
        oldCar = CarModel.query.filter_by(plate_number=plate_number).first()
        if oldCar:
            raise Exception('plate should be unique')
        if (not len(gate_ids) > 0 and not all_gates):
            raise Exception('gate_ids should be provided')
        if (all_gates):
            gate_ids = [gate.id for gate in GateModel.get_all()]
        carInfo = CarModel(owner_name, plate_number, color, gate_ids)
        db.session.add(carInfo)
        db.session.commit()
        return AddCar(car=carInfo)


class BlockCar(graphene.Mutation):
    car = graphene.Field(Car)

    class Arguments:
        car_id = graphene.String(required=True)

    @mutation_header_jwt_required
    def mutate(self, info, car_id):
        car = CarModel.query.filter_by(id=car_id).first()
        if car == None:
            raise Exception('car not found')
        CarModel.update(car, blocked=True, blocked_at=datetime.now())
        return BlockCar(car=car)


class UnBlockCar(graphene.Mutation):
    car = graphene.Field(Car)

    class Arguments:
        car_id = graphene.String(required=True)

    @mutation_header_jwt_required
    def mutate(self, info, car_id):
        car = CarModel.query.filter_by(id=car_id).first()
        if car == None:
            raise Exception('car not found')
        CarModel.update(car, blocked=False, blocked_at=None)
        return BlockCar(car=car)


class ValidateCar(graphene.Mutation):
    car = graphene.Field(Car)
    access = graphene.Boolean()

    class Arguments:
        plate_number = graphene.String(required=True)
        gate_id = graphene.String(required=True)
        color = graphene.String(required=True)

    def mutate(self, info, plate_number, gate_id, color):
        car = CarModel.query.filter_by(
            plate_number=plate_number, color=color).first()
        if car == None:
            print('car not found')
            send_notification(gate_id, plate_number)
            return ValidateCar(car=car, access=False)
        if (not uuid.UUID(gate_id) in car.gate_ids):
            return ValidateCar(car=car, access=False)
        access = not car.blocked
        if (access):
            history = HistoryModel(car_id=car.id, gate_id=gate_id)
            db.session.add(history)
            db.session.commit()
        return ValidateCar(car=car, access=access)
