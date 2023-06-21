from models import BaseModelMixin
from ext import db
from sqlalchemy.dialects.postgresql import UUID,ARRAY


class Notification(BaseModelMixin):
    __tablename__= 'notifications'
    body=db.Column(db.String(255),nullable=False)
    title=db.Column(db.String(255),nullable=False)
    link=db.Column(db.String(255),nullable=True)
    def __init__(self,body, title, link=None):
        self.body = body
        self.title = title
        self.link = link
    def __repr__(self):
        return f'<Notification {self.id}>'