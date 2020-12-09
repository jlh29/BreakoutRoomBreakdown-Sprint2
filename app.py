"""
    This module handles the Flask application and receiving and responding to
    data over socketio.
"""
# pylint: disable=fixme
# pylint: disable=duplicate-code
import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import db_instance
import db_utils
import login_utils
import models
import scheduled_tasks
import socket_utils
from socket_utils import SOCKET
from api_twilio import Twilio
from api_sendgrid import SendGrid

load_dotenv(join(dirname(__file__), "sql.env"))

APP = flask.Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

USERS_UPDATED_CHANNEL = "users updated"

USER_LOGIN_CHANNEL = "new login"
USER_LOGIN_NAME_KEY = "name"
USER_LOGIN_TOKEN_KEY = "idToken"
USER_LOGIN_ROLE_KEY = "role"

SUCCESSFUL_LOGIN_CHANNEL = "successful login"
FAILED_LOGIN_CHANNEL = "failed login"

TIME_AVAILABILITY_REQUEST_CHANNEL = "time availability request"
TIME_AVAILABILITY_RESPONSE_CHANNEL = "time availability response"
ALL_TIMES_KEY = "times"

DATE_AVAILABILITY_REQUEST_CHANNEL = "date availability request"
DATE_AVAILABILITY_RESPONSE_CHANNEL = "date availability response"
ALL_DATES_KEY = "dates"

RESERVATION_SUBMIT_CHANNEL = "reservation submit"
RESERVATION_RESPONSE_CHANNEL = "reservation response"
RESERVATION_SUCCESS_KEY = "successful"
RESERVATION_KEY = "reservation"
CONNECT_CHANNEL = "connect"
DISCONNECT_CHANNEL = "disconnect"

LIBRARIAN_DATA_REQUEST_CHANNEL = "overview request"
UPDATE_ROOM_CHANNEL = "update room"
UPDATE_USER_CHANNEL = "update user"

APPOINTMENTS_REQUEST_CHANNEL = "appointments request"
APPOINTMENTS_RESPONSE_CHANNEL = "appointments response"
APPOINTMENTS_KEY = "appointments"
APPOINTMENTS_REQUEST_DATE_KEY = "date"
APPOINTMENTS_REQUEST_DATE_FORMAT = "%m/%d/%Y"

USERS_REQUEST_CHANNEL = "users request"
USERS_RESPONSE_CHANNEL = "users response"
USERS_KEY = "users"

ROOMS_REQUEST_CHANNEL = "rooms request"
ROOMS_RESPONSE_CHANNEL = "rooms response"
ROOMS_KEY = "rooms"

CHECK_IN_CHANNEL = "check in"
CHECK_IN_RESPONSE_CHANNEL = "check in response"
CHECK_IN_CODE_KEY = "code"
CHECK_IN_SUCCESS_KEY = "successful"

DATE_KEY = "date"
TIME_KEY = "time"
ATTENDEES_KEY = "attendees"
PHONE_NUMBER_KEY = "phoneNumber"
TIMESLOT_KEY = "timeslot"
TIME_AVAILABILITY_KEY = "isAvailable"
AVAILABLE_ROOMS_KEY = "availableRooms"
DATE_FORMAT = "%m/%d/%Y"

DISABLE_DATE = "disable date"
DISABLE_CHANNEL = "disable channel"
DATE_RANGE = "date range"
START_DATE = "start date"
END_DATE = "end date"
NOTE = "note"

STUDENT_DATE_AVAILABILITY_RANGE = 3
PROFESSOR_DATE_AVAILABILITY_RANGE = 7

EST_TZ_OFFSET = datetime.timezone(datetime.timedelta(hours=-5))

CONNECTED_USERS = {}


def _current_user_role():
    """
    Returns the currently communicating client's UserRole
    """
    if flask.request.sid not in CONNECTED_USERS:
        return None
    return CONNECTED_USERS[flask.request.sid].role


def emit_all_dates(channel):
    """
    Send all disable dates to the client
    """
    all_start_dates, all_end_dates, all_notes = db_utils.get_disable_date()

    all_start_dates = [str(x.date()) for x in all_start_dates]
    all_end_dates = [str(x.date()) for x in all_end_dates]

    date_range = list(list(x) for x in zip(all_start_dates, all_end_dates))

    SOCKET.emit(
        channel,
        {
            DATE_RANGE: date_range,
            START_DATE: all_start_dates,
            END_DATE: all_end_dates,
            NOTE: all_notes,
        },
    )
    print("Data sent to client")


@SOCKET.on(CONNECT_CHANNEL)
def on_connect():
    """
    Called whenever a user connects
    """
    print("Someone connected!")


@SOCKET.on(DISCONNECT_CHANNEL)
def on_disconnect():
    """
    Called whenever a user disconnects
    """
    print("Someone disconnected!")
    CONNECTED_USERS.pop(flask.request.sid, None)


@SOCKET.on(USER_LOGIN_CHANNEL)
def on_new_user_login(data):
    """
    Called whenever a user successfully passes through the Google OAuth login
    Sends the user's name and role back to the client so that the webpage
    is rendered correctly
    """
    print(f"Got an event for new user login")
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            USER_LOGIN_TOKEN_KEY in data,
        ]
    )
    assert flask.request.sid is not None
    auth_user = login_utils.get_user_from_google_token(data[USER_LOGIN_TOKEN_KEY])
    if auth_user is None:
        SOCKET.emit(
            FAILED_LOGIN_CHANNEL,
            room=flask.request.sid,
        )
        return
    CONNECTED_USERS[flask.request.sid] = auth_user
    SOCKET.emit(
        SUCCESSFUL_LOGIN_CHANNEL,
        {
            USER_LOGIN_NAME_KEY: auth_user.name,
            USER_LOGIN_ROLE_KEY: auth_user.role.value,
        },
        room=flask.request.sid,
    )
    emit_all_dates(DISABLE_CHANNEL)


@SOCKET.on(DATE_AVAILABILITY_REQUEST_CHANNEL)
def on_date_availability_request(data):
    """
    Called whenever the reservation form is first loaded
    Returns a list of dates that are not fully booked or otherwise unavailable
    """
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            DATE_KEY in data,
        ]
    )
    assert isinstance(data[DATE_KEY], str)
    print("Got an event for date input with data:", data)
    date = datetime.datetime.strptime(data[DATE_KEY], DATE_FORMAT)
    user_role = _current_user_role()
    if user_role == models.UserRole.LIBRARIAN:
        available_dates = db_utils.get_available_dates_for_month(date=date)
    elif user_role == models.UserRole.PROFESSOR:
        available_dates = db_utils.get_available_dates_after_date(
            date=date,
            date_range=PROFESSOR_DATE_AVAILABILITY_RANGE,
        )
    elif user_role == models.UserRole.STUDENT:
        available_dates = db_utils.get_available_dates_after_date(
            date=date,
            date_range=STUDENT_DATE_AVAILABILITY_RANGE,
        )
    else:
        return
    available_date_timestamps = [
        available_date.timestamp() * 1000.0 for available_date in available_dates
    ]
    SOCKET.emit(
        DATE_AVAILABILITY_RESPONSE_CHANNEL,
        {ALL_DATES_KEY: available_date_timestamps},
        room=flask.request.sid,
    )


@SOCKET.on(TIME_AVAILABILITY_REQUEST_CHANNEL)
def on_time_availability_request(data):
    """
    Called whenever a user clicks on a date in the reservation form
    Checks to see what timeslots are available and sends them to the client
    """
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            DATE_KEY in data,
        ]
    )
    assert isinstance(data[DATE_KEY], str)
    print("Got an event for time input with data:", data)
    if _current_user_role() is None:
        return
    date = datetime.datetime.strptime(data[DATE_KEY], DATE_FORMAT)
    available_times = db_utils.get_available_times_for_date(date=date.date())
    # TODO: jlh29, extend this for timeslots that are not 2 hours
    all_times = [
        {
            TIMESLOT_KEY: f"{hour}:00-{hour+2}:00",
            AVAILABLE_ROOMS_KEY: available_times[hour],
            TIME_AVAILABILITY_KEY: available_times[hour] != 0,
        }
        for hour in sorted(available_times)
    ]
    SOCKET.emit(
        TIME_AVAILABILITY_RESPONSE_CHANNEL,
        {ALL_TIMES_KEY: all_times},
        room=flask.request.sid,
    )


@SOCKET.on(RESERVATION_SUBMIT_CHANNEL)
def on_reservation_submit(data):
    """
    Called whenever a user submits the reservation form
    Creates a new Appointment (if possible) and returns its details
    """
    print("running")
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            DATE_KEY in data,
            TIME_KEY in data,
            PHONE_NUMBER_KEY in data,
            ATTENDEES_KEY in data,
        ]
    )
    assert all(
        [
            isinstance(data[DATE_KEY], (float, int)),
            isinstance(data[TIME_KEY], str),
            isinstance(data[PHONE_NUMBER_KEY], (str, int)),
            data[ATTENDEES_KEY] is None
            or (
                isinstance(data[ATTENDEES_KEY], list)
                and all([isinstance(attendee, str) for attendee in data[ATTENDEES_KEY]])
            ),
        ]
    )
    user_role = _current_user_role()
    date = datetime.datetime.fromtimestamp(data[DATE_KEY] / 1000.0)
    date_difference = (date - datetime.datetime.utcnow()).days
    if user_role is None:
        return
    if (
            user_role == models.UserRole.STUDENT
            and date_difference > STUDENT_DATE_AVAILABILITY_RANGE
    ):
        return
    if (
            user_role == models.UserRole.PROFESSOR
            and date_difference > PROFESSOR_DATE_AVAILABILITY_RANGE
    ):
        return
    attendee_ids = db_utils.get_attendee_ids_from_ucids(data[ATTENDEES_KEY])
    # TODO: jlh29, actually allow the user to choose a room
    available_rooms_by_time = db_utils.get_available_room_ids_for_date(date.date())
    # TODO: jlh29, fix this messy messy messy code for Sprint 2
    selected_hour = int(data[TIME_KEY].split(":")[0])
    if len(available_rooms_by_time[selected_hour]) == 0:
        return
    room_id = available_rooms_by_time[selected_hour][0]
    # TODO: jlh29, fix this time/date mess
    start_time_string, end_time_string = data[TIME_KEY].split("-")
    start_time = datetime.datetime(
        date.year,
        date.month,
        date.day,
        int(start_time_string.split(":")[0]),
        0,
        0,
        tzinfo=EST_TZ_OFFSET,
    )
    end_time = datetime.datetime(
        date.year,
        date.month,
        date.day,
        int(end_time_string.split(":")[0]),
        0,
        0,
        tzinfo=EST_TZ_OFFSET,
    )
    organizer_id = CONNECTED_USERS[flask.request.sid].id
    (
        reservation_success,
        reservation_code,
        reservation_dict,
    ) = db_utils.create_reservation(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        organizer_id=organizer_id,
        attendee_ids=attendee_ids,
    )

    ucid = CONNECTED_USERS[flask.request.sid].ucid
    if reservation_success:
        send_confirmation(
            number=data[PHONE_NUMBER_KEY],
            ucid=ucid,
            date=date.date(),
            time=data[TIME_KEY],
            attendees=data[ATTENDEES_KEY],
            confirmation=reservation_code,
        )

    SOCKET.emit(
        RESERVATION_RESPONSE_CHANNEL,
        {
            RESERVATION_SUCCESS_KEY: reservation_success,
            CHECK_IN_CODE_KEY: reservation_code,
            RESERVATION_KEY: reservation_dict,
        },
        room=flask.request.sid,
    )


def send_confirmation(number, ucid, date, time, attendees, confirmation):
    """
    Sends the confirmation through text, if number is invalid send via email
    """
    email = "{}@njit.edu".format(ucid)
    try:
        to_number = "+1{}".format(number)
        twilio = Twilio(to_number)
        twilio.send_text(date, time, attendees, confirmation)
        print("Text message sent!")

    except:
        sendgrid = SendGrid(email)
        sendgrid.send_email(date, time, attendees, confirmation)
        print("Email sent!")


@APP.route("/")
def index():
    """
    Provides the client with the main webpage
    """

    return flask.render_template("index.html")


@APP.route("/about")
def about():
    """
    Provides the client with the landing page
    """

    return flask.render_template("about.html")


@SOCKET.on(LIBRARIAN_DATA_REQUEST_CHANNEL)
def on_librarian_data_request(data):
    """
    Called whenever the Librarian Overview UI first loads to obtain all
    essential information simultaneously
    """
    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return
    on_request_appointments(data)
    on_request_rooms()
    on_request_users()


@SOCKET.on(APPOINTMENTS_REQUEST_CHANNEL)
def on_request_appointments(data):
    """
    Called whenever the librarian clicks on a date in the Librarian Overview
    UI
    Returns a list of all Appointments for a given date
    """
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            DATE_KEY in data,
        ]
    )
    assert isinstance(data[DATE_KEY], str)
    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return
    date = datetime.datetime.strptime(data[DATE_KEY], DATE_FORMAT)
    appointments = db_utils.get_all_appointments_for_date(
        date=date,
        as_dicts=True,
    )
    SOCKET.emit(
        APPOINTMENTS_RESPONSE_CHANNEL,
        {APPOINTMENTS_KEY: appointments},
        room=flask.request.sid,
    )


@SOCKET.on(USERS_REQUEST_CHANNEL)
def on_request_users():
    """
    Called whenever the Librarian Overview UI loads the User Overview section
    Returns a list of all AuthUsers
    """
    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return
    users = db_utils.get_all_user_objs(as_dicts=True)
    SOCKET.emit(
        USERS_RESPONSE_CHANNEL,
        {USERS_KEY: users},
        room=flask.request.sid,
    )


@SOCKET.on(ROOMS_REQUEST_CHANNEL)
def on_request_rooms():
    """
    Called whenever the Librarian Overview UI loads the Room Overview section
    Returns a list of all BreakoutRooms
    """
    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return
    rooms = db_utils.get_all_room_objs(as_dicts=True)
    SOCKET.emit(
        ROOMS_RESPONSE_CHANNEL,
        {ROOMS_KEY: rooms},
        room=flask.request.sid,
    )


@SOCKET.on(CHECK_IN_CHANNEL)
def on_check_in(data):
    """
    Called whenever the librarian checks in a group via their check-in code
    """
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            CHECK_IN_CODE_KEY in data,
        ]
    )
    assert isinstance(data[CHECK_IN_CODE_KEY], str)
    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return
    check_in_code = data[CHECK_IN_CODE_KEY]
    result = db_utils.check_in_with_code(check_in_code=check_in_code)
    SOCKET.emit(
        CHECK_IN_RESPONSE_CHANNEL,
        {CHECK_IN_SUCCESS_KEY: result},
        room=flask.request.sid,
    )


@SOCKET.on(DISABLE_DATE)
def on_disable_date(data):
    """
    Called whenever the librarian set a date to disable in the calendar
    """
    print("Got an event for new date input with data:", data)

    start_date = datetime.datetime.strptime(data["startDate"], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(data["endDate"], "%Y-%m-%d")
    note = data["note"]

    db_utils.add_disable_date(start_date, end_date, note)
    emit_all_dates(DISABLE_CHANNEL)


@SOCKET.on(UPDATE_ROOM_CHANNEL)
def on_update_room(data):
    """
    Called whenever the librarian makes an edit to a room in the Librarian Overview
    """
    assert data is not None
    assert isinstance(data, dict)
    assert set(models.BreakoutRoom._fields).issubset(data)
    assert all(
        [
            isinstance(data["id"], int),
            isinstance(data["room_number"], (int, str)),
            isinstance(data["size"], str),
            isinstance(data["capacity"], (int, str)),
        ]
    )

    try:
        room_size = models.RoomSize(data["size"].lower())
    except ValueError:
        print("Invalid value of 'size' passed to server when updating a room")
        room_size = None
    try:
        room_capacity = int(data["capacity"])
    except ValueError:
        print("Invalid value of 'capacity' passed to server when updating a room")
        room_capacity = None

    assert room_size is not None
    assert room_capacity is not None

    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return

    db_utils.update_room(
        room_id=data["id"],
        room_number=data["room_number"],
        size=room_size,
        capacity=room_capacity,
    )

    on_request_rooms()


@SOCKET.on(UPDATE_USER_CHANNEL)
def on_update_user(data):
    """
    Called whenever the librarian makes an edit to a room in the Librarian Overview
    """
    assert data is not None
    assert all(
        [
            isinstance(data, dict),
            "id" in data,
            "role" in data,
        ]
    )
    assert all(
        [
            isinstance(data["id"], int),
            isinstance(data["role"], str),
        ]
    )

    try:
        role = models.UserRole(data["role"].lower())
    except ValueError:
        print("Invalid value of 'role' passed to server when updating a user")
        role = None

    assert role is not None

    if not _current_user_role() == models.UserRole.LIBRARIAN:
        return

    db_utils.update_user_role(
        user_id=data["id"],
        role=role,
    )

    on_request_users()


if __name__ == "__main__":
    db_instance.init_db(APP)
    socket_utils.init_socket(APP)
    scheduled_tasks.start_tasks()
    SOCKET.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
