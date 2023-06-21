from models import BaseModelMixin
from ext import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY
class User(BaseModelMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80))
    fcm_tokens = db.Column(ARRAY(db.String(255)), unique=False, nullable=True)
    
    def __init__(self, username, password, name, email,fcm_tokens=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.fcm_tokens = fcm_tokens
    def __repr__(self):
        return f'<User {self.username}>'
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)    