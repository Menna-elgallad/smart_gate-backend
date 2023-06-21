from models import BaseModelMixin
from ext import db
from sqlalchemy.dialects.postgresql import UUID


class History(BaseModelMixin):
    __tablename__= 'history'
    gate_id=db.Column(UUID(as_uuid=True))
    car_id=db.Column(UUID(as_uuid=True))

    def __init__(self, gate_id, car_id):
        self.gate_id = gate_id
        self.car_id = car_id
    def __repr__(self):
        return f'<History {self.created}>'
