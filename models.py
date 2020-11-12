import flask_sqlalchemy
from app import db
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
        
class Attendee(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    attendee = DB.Column(DB.String(120))
    
    appointmentID = DB.Column(DB.Integer, DB.ForeignKey("appointment.id"), nullable=False)
    
    def __init__(self, attendee, appointmentID):
        self.attendee = attendee
        self.appointmentID = appointmentID
        
class Appointment(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    organizer = DB.Column(DB.String(120))
    numberOfAttendees = DB.Column(DB.Integer)
    roomSize = DB.Column(DB.String(2))
    # roomNumber = DB.Column(DB.Integer)
    reservation = DB.Column(DB.DateTime())
    
    attendees = DB.relationship(Attendee, backref="Appointment", lazy="True")
    
    def __init__(self, organizer, numberOfAttendees, roomSize, reservation):
        self.organizer = organizer
        self.numberOfAttendees = numberOfAttendees
        self.roomSize = roomSize
        self.reservation = reservation
    

class AuthUserType(Enum):
    GOOGLE = "google"
    PASSWORD = "password"