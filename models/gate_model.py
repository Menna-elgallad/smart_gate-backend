from models import BaseModelMixin
from ext import db
from sqlalchemy.orm import relationship


class Gate(BaseModelMixin):
    __tablename__= 'gates'
    name=db.Column(db.String(80),unique=True,nullable=False)
    description=db.Column(db.String(255),nullable=False)
    lat=db.Column(db.String(255),nullable=False)
    long=db.Column(db.String(255),nullable=False)
    # cars=relationship('Car', back_populates="gate")
    # cameras=relationship('Camera', back_populates="gate")

    def __init__(self, name, description, lat, long):
        self.name = name
        self.description = description
        self.lat = lat
        self.long = long
    def __repr__(self):
        return f'<Gate {self.name}>'
