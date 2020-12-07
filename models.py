"""
    This module defines the structure of the PostgreSQL database and related
    data structures
"""
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
from collections import namedtuple
import datetime
from enum import Enum
from db_instance import DB

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
        "status",
    ],
)


class AuthUser(DB.Model):
    """
    This model defines a user that has signed in with OAuth
    """

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
        assert isinstance(ucid, str) and len(ucid) > 0
        assert isinstance(name, str) and len(name) > 0
        self.name = name
        self.auth_type = auth_type.value
        self.ucid = ucid
        self.role = role.value

    def __repr__(self):
        return f"<User name: {self.name}" f"\trole: {self.role}" f"\tucid: {self.ucid}>"

    def get_email(self):
        """
        Returns the generated email address for a given AuthUser
        """
        return f"{self.ucid}@njit.edu"


class Attendee(DB.Model):
    """
    This model defines each of the participants in an appointment
    """

    id = DB.Column(DB.Integer, primary_key=True)
    ucid = DB.Column(DB.String(120), nullable=False)

    def __init__(self, ucid):
        assert isinstance(ucid, str) and len(ucid) > 0
        self.ucid = ucid

    def __repr__(self):
        return f"<Attendee ucid: {self.ucid}>"

    def get_email(self):
        """
        Returns the generated email address for a given Attendee
        """
        return f"{self.ucid}@njit.edu"


class Appointment(DB.Model):
    """
    This model defines a breakout room reservation
    """

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
        assert isinstance(room_id, int)
        assert isinstance(start_time, datetime.datetime)
        assert isinstance(end_time, datetime.datetime)
        assert isinstance(organizer_id, int)
        assert attendee_ids is None or (
            isinstance(attendee_ids, list)
            and all([isinstance(attendee, int) for attendee in attendee_ids])
        )
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time
        self.organizer_id = organizer_id
        self.attendee_ids = attendee_ids
        self.status = AppointmentStatus.WAITING.value

    def __repr__(self):
        return (
            f"<Appointment room id: {self.room_id}\tstart time: {self.start_time}"
            f"\tend time: {self.end_time}\torganizer id: {self.organizer_id}"
            f"\tattendee ids: {self.attendee_ids}\tstatus: {self.status}>"
        )


class Room(DB.Model):
    """
    This model defines a breakout room's information
    """

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
        assert isinstance(room_number, (int, str))
        assert isinstance(capacity, int) and capacity > 0
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

    def __repr__(self):
        return (
            f"<Room number: {self.room_number}\tcapacity: {self.capacity}"
            f"\tsize: {self.size}>"
        )


class UnavailableDate(DB.Model):
    """
    This model defines a date that the librarian has made unavailable
    """

    date = DB.Column(DB.DateTime, primary_key=True)
    reason = DB.Column(DB.String(150), nullable=True)

    def __init__(self, date, reason=None):
        assert isinstance(date, datetime.datetime)
        self.date = date
        self.reason = reason

    def __repr__(self):
        return f"<Unavailable Date: {self.date}\treason: {self.reason}>"


class CheckIn(DB.Model):
    """
    This model defines the check-in code for each appointment
    """

    id = DB.Column(DB.Integer, primary_key=True)
    reservation_id = DB.Column(
        DB.Integer, DB.ForeignKey("appointment.id"), nullable=False
    )
    validation_code = DB.Column(DB.String(32), nullable=False)

    def __init__(self, reservation_id, validation_code):
        self.reservation_id = reservation_id
        self.validation_code = validation_code

    def __repr__(self):
        return (
            f"<CheckIn reservation ID: {self.reservation_id}\t"
            f"validation code: {self.validation_code}>"
        )


class AuthUserType(Enum):
    """
    Defines the possible login types
    """

    GOOGLE = "google"
    PASSWORD = "password"


class UserRole(Enum):
    """
    Defines the possible set of permissions that a user can have
    """

    LIBRARIAN = "librarian"
    PROFESSOR = "professor"
    STUDENT = "student"


class RoomSize(Enum):
    """
    Defines the qualitative size of a breakout room
    """

    SMALL = "s"
    MEDIUM = "m"
    LARGE = "l"
    XLARGE = "xl"


class AppointmentStatus(Enum):
    """
    Defines the possible check-in statuses of an appointment
    """

    CHECKED_IN = "checked-in"
    WAITING = "waiting"
    FREE = "free"
