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
    room_id = DB.Column(DB.Integer, DB.ForeignKey("room.id"), nullable=False)
    reservation = DB.Column(DB.DateTime())
    
    attendees = DB.relationship(Attendee, backref="Appointment", lazy="True")
    
    def __init__(self, organizer, numberOfAttendees, roomSize, reservation):
        self.organizer = organizer
        self.numberOfAttendees = numberOfAttendees
        self.roomSize = roomSize
        self.reservation = reservation

class Room(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room_number = DB.Column(DB.String(40), nullable=False, unique=True)
    size = DB.Column(DB.String(4), nullable=False)
    capacity = DB.Column(DB.Integer)
    appointments = DB.relationship(Appointment, backref="Room", lazy="True")

    def __init__(self, room_number, capacity, size=None):
        assert capacity > 0
        if size is not None:
            assert isinstance(size, RoomSize)
        elif capacity < 3:
            size = RoomSize.SMALL
        elif capacity < 6:
            size = RoomSize.MEDIUM
        elif capacity < 9:
            size = RoomSize.LARGE
        else:
            size = RoomSize.XLARGE

        self.room_number = room_number
        self.capacity = capacity
        self.size = size.value

class AuthUserType(Enum):
    GOOGLE = "google"
    PASSWORD = "password"

class UserRole(Enum):
    LIBRARIAN = "librarian"
    PROFESSOR = "professor"
    STUDENT = "student"

class RoomSize(Enum):
    SMALL = "s"
    MEDIUM = "m"
    LARGE = "l"
    XLARGE = "xl"
