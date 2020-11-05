import flask_sqlalchemy
from db_utils import DB
from enum import Enum

class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    name = DB.Column(DB.String(120))
    
    def __init__(self, name, auth_type):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    GOOGLE = "google"
    PASSWORD = "password"