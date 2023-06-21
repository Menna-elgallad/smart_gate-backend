from models import BaseModelMixin
from ext import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Camera(BaseModelMixin):
    __tablename__= 'cameras'
    name=db.Column(db.String(80),unique=True,nullable=False)
    description=db.Column(db.String(255),nullable=False)
    url=db.Column(db.String(255),nullable=False)
    api_url=db.Column(db.String(255),nullable=True)
    gate_id=db.Column(UUID(as_uuid=True),db.ForeignKey("gates.id"))

    def __init__(self, name, description, url, api_url , gate_id):
        self.name = name
        self.description = description
        self.url = url
        self.api_url = api_url
        self.gate_id = gate_id
    def __repr__(self):
        return f'<Camera {self.name}>'