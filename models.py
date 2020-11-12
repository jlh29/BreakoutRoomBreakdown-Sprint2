import datetime
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
    appointments = DB.relationship("Appointment", backref="organizer", lazy="True")

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
    attendee_ucid = DB.Column(DB.String(120))

    def __init__(self, attendee_ucid):
        self.attendee_ucid = attendee_ucid
        
class Appointment(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room_id = DB.Column(DB.Integer, DB.ForeignKey("room.id"), nullable=False)
    start_time = DB.Column(DB.DateTime, nullable=False)
    end_time = DB.Column(DB.DateTime, nullable=False)
    organizer_id = DB.Column(DB.Integer, DB.ForeignKey("AuthUser.id"), nullable=False)
    attendee_ids = DB.Column(DB.ARRAY(DB.Integer))

    attendee_relation = DB.relationship(Attendee, backref="appointment", lazy="True")

    def __init__(self, room_id, start_time, end_time, organizer_id, attendee_ids=None):
        assert isinstance(start_time, datetime.datetime)
        assert isinstance(end_time, datetime.datetime)
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time
        self.organizer_id = organizer_id
        self.attendee_ids = attendee_ids

class Room(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room_number = DB.Column(DB.String(40), nullable=False, unique=True)
    size = DB.Column(DB.String(4), nullable=False)
    capacity = DB.Column(DB.Integer)
    appointments = DB.relationship(Appointment, backref="room", lazy="True")

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
