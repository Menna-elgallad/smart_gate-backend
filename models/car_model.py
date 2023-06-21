from models import BaseModelMixin
from ext import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID,ARRAY


class Car(BaseModelMixin):
    __tablename__ = 'cars'
    owner_name = db.Column(db.String(60), nullable=False)
    plate_number = db.Column(db.String(120), nullable=False)
    color = db.Column(db.String(60), nullable=True)
    blocked = db.Column(db.Boolean(), default=False)
    blocked_at = db.Column(db.DateTime, nullable=True)
    gate_ids = db.Column(ARRAY(UUID(as_uuid=True)))
    # gate = relationship("Gate", back_populates="cameras")

    def __init__(self, owner_name, plate_number, color, gate_ids, blocked=False, blocked_at=None):
        self.owner_name = owner_name
        self.plate_number = plate_number
        self.color = color
        self.blocked = blocked
        self.blocked_at = blocked_at
        self.gate_ids = gate_ids

    def __repr__(self):
        return f'<Car {self.plate_number}>'
