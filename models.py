from collections import namedtuple
import datetime
import flask_sqlalchemy
from db_instance import DB
from enum import Enum

UserInfo = namedtuple("UserInfo", ["id", "ucid", "role", "name"])
AttendeeInfo = namedtuple("AttendeeInfo", ["id", "ucid"])
BreakoutRoom = namedtuple("BreakoutRoom", ["id", "room_number", "size", "capacity"])
AppointmentInfo = namedtuple(
    "AppointmentInfo", 
    [
        "id",
        "room",
        "start_time",
        "end_time",
        "organizer",
        "attendees",
    ],
)

class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    ucid = DB.Column(DB.String(120), nullable=False)
    auth_type = DB.Column(DB.String(120), nullable=False)
    role = DB.Column(DB.String(120), nullable=False)
    name = DB.Column(DB.String(120))
    appointments = DB.relationship(
        "Appointment",
        backref="organizer",
        lazy="dynamic",
        primaryjoin="Appointment.organizer_id == AuthUser.id",
    )

    def __init__(self, ucid, auth_type, role, name):
        assert isinstance(auth_type, AuthUserType)
        assert isinstance(role, UserRole)
        self.name = name
        self.auth_type = auth_type.value
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
    ucid = DB.Column(DB.String(120), nullable=False)

    def __init__(self, ucid):
        self.ucid = ucid

    def get_email(self):
        return f"{self.ucid}@njit.edu"

class Appointment(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room_id = DB.Column(DB.Integer, DB.ForeignKey("room.id"), nullable=False)
    start_time = DB.Column(DB.DateTime, nullable=False)
    end_time = DB.Column(DB.DateTime, nullable=False)
    organizer_id = DB.Column(DB.Integer, DB.ForeignKey("auth_user.id"), nullable=False)
    attendee_ids = DB.Column(DB.ARRAY(DB.Integer))
    status = DB.Column(DB.String(20), nullable=False)

    checkin_relation = DB.relationship(
        "CheckIn",
        backref="appointment",
        lazy="dynamic",
        primaryjoin="CheckIn.reservation_id == Appointment.id",
    )

    def __init__(self, room_id, start_time, end_time, organizer_id, attendee_ids=None):
        assert isinstance(start_time, datetime.datetime)
        assert isinstance(end_time, datetime.datetime)
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time
        self.organizer_id = organizer_id
        self.attendee_ids = attendee_ids
        self.status = AppointmentStatus.WAITING.value

class Room(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    room_number = DB.Column(DB.String(40), nullable=False, unique=True)
    size = DB.Column(DB.String(4), nullable=False)
    capacity = DB.Column(DB.Integer)
    appointments = DB.relationship(
        "Appointment",
        backref="room",
        lazy="dynamic",
        primaryjoin="Appointment.room_id == Room.id",
    )

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

class UnavailableDate(DB.Model):
    date = DB.Column(DB.DateTime, primary_key=True)
    reason = DB.Column(DB.String(150), nullable=True)

    def __init__(self, date, reason=None):
        assert isinstance(date, datetime.datetime)
        self.date = date
        self.reason = reason

    def __repr__(self):
        return (f"<Unavailable Date: {self.date}\treason: {self.reason}>")

class CheckIn(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    reservation_id = DB.Column(DB.Integer, DB.ForeignKey("appointment.id"), nullable=False)
    validation_code = DB.Column(DB.String(32), nullable=False)

    def __init__(self, reservation_id, validation_code):
        self.reservation_id = reservation_id
        self.validation_code = validation_code

    def __repr__(self):
        return (f"<CheckIn reservation ID: {self.reservation_id}\t"
                f"validation code: {self.validation_code}>")

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

class AppointmentStatus(Enum):
    CHECKED_IN = "checked-in"
    WAITING = "waiting"
    FREE = "free"
