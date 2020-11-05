import flask_sqlalchemy
from app import db
from enum import Enum

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    
    def __init__(self, name, auth_type):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    GOOGLE = "google"
    PASSWORD = "password"