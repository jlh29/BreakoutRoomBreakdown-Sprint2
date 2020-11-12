import flask_sqlalchemy
from app import db
from db_utils import DB
from enum import Enum

class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    ucid = DB.Column(DB.String(120), nullable=False)
    auth_type = DB.Column(DB.String(120), nullable=False)
    role = DB.Column(DB.String(120), nullable=False)
    name = DB.Column(DB.String(120))

    def __init__(self, ucid, auth_type, role, name):
        assert isinstance(auth_type, AuthUserType)
        assert isinstance(role, UserRole)
        self.name = name
        self.auth_type = auth_type
        self.ucid = ucid
        self.role = role.value

    def __repr__(self):
        return (f"<User name: {self.name}"
                f"\trole: {self.role}"
                f"\tucid: {self.ucid}>")

    def get_email(self):
        return f"{self.ucid}@njit.edu"

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

class UserRole(Enum):
    LIBRARIAN = "librarian"
    PROFESSOR = "professor"
    STUDENT = "student"
