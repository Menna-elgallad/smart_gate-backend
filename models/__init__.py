import sqlalchemy.orm.exc
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID

from ext import db
from utils import logger
import uuid


class BaseModelMixin(db.Model):

    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    @classmethod
    def create(cls, **kwargs):
        b = cls(**kwargs)
        db.session.add(b)
        db.session.commit()
        return b

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def get_all(cls, start=0, limit=None):
        q = cls.query.order_by(cls.id.desc())
        if not any([start, limit]):
            return q.all()
        return q[start:start + limit]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except sqlalchemy.orm.exc.ObjectDeletedError:
            db.session.rollback()
            logger.warn(
                'Error during deleting: Object %s already deleted', self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash((self.__class__, self.id))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
