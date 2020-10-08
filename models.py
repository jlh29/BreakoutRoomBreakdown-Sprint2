# models.py
import flask_sqlalchemy
from app import db


class GoogleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<User name: {}".format(self.name)

