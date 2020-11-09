import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_socketio
import db_instance
from db_instance import DB
import db_utils
import models 
import socket_utils
from socket_utils import SOCKET

load_dotenv(join(dirname(__file__), "sql.env"))

APP = flask.Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

USERS_UPDATED_CHANNEL = "users updated"

USER_LOGIN_CHANNEL = "new login"
USER_LOGIN_NAME_KEY = "name"
USER_LOGIN_EMAIL_KEY = "email"

SUCCESSFUL_LOGIN_CHANNEL = "successful login"

TIME_AVAILABILITY_REQUEST_CHANNEL = "time availability request"
TIME_AVAILABILITY_RESPONSE_CHANNEL = "time availability response"
ALL_TIMES_KEY = "times"

DATE_AVAILABILITY_REQUEST_CHANNEL = "date availability request"
DATE_AVAILABILITY_RESPONSE_CHANNEL = "date availability response"
ALL_DATES_KEY = "dates"

RESERVATION_SUBMIT_CHANNEL = "reservation submit"
RESERVATION_RESPONSE_CHANNEL = "reservation response"
CONNECT_CHANNEL = "connect"
DISCONNECT_CHANNEL = "disconnect"

LIBRARIAN_DATA_REQUEST_CHANNEL = "overview request"

APPOINTMENTS_REQUEST_CHANNEL = "appointments request"
APPOINTMENTS_RESPONSE_CHANNEL = "appointments response"
APPOINTMENTS_KEY = "appointments"

USERS_REQUEST_CHANNEL = "users request"
USERS_RESPONSE_CHANNEL = "users response"
USERS_KEY = "users"

ROOMS_REQUEST_CHANNEL = "rooms request"
ROOMS_RESPONSE_CHANNEL = "rooms response"
ROOMS_KEY = "rooms"

DATE_KEY = "date"
TIME_KEY = "time"
ATTENDEES_KEY = "attendees"
TIMESLOT_KEY = "timeslot"
TIME_AVAILABILITY_KEY = "isAvailable"
AVAILABLE_ROOMS_KEY = "availableRooms"

CONNECTED_USERS = {}

@SOCKET.on(CONNECT_CHANNEL)
def on_connect():
    print("Someone connected!")
    
@SOCKET.on(DISCONNECT_CHANNEL)
def on_disconnect():
    print ("Someone disconnected!")
    CONNECTED_USERS.pop(flask.request.sid, None)
    
@SOCKET.on(USER_LOGIN_CHANNEL)
def on_new_user_login(data):
    print(f"Got an event for new user login with data: {data}")
    name = data[USER_LOGIN_NAME_KEY]
    ucid = data[USER_LOGIN_EMAIL_KEY].split("@")[0]
    CONNECTED_USERS[flask.request.sid] = db_utils.add_or_get_auth_user(ucid, name)
    SOCKET.emit(
        SUCCESSFUL_LOGIN_CHANNEL,
        {USER_LOGIN_NAME_KEY: name},
        room=flask.request.sid,
    )

@SOCKET.on(DATE_AVAILABILITY_REQUEST_CHANNEL)
def on_date_availability_request(data):
    print("Got an event for date input with data:", data)
    date = datetime.datetime.fromtimestamp(data[DATE_KEY] / 1000.0)
    available_dates = db_utils.get_available_dates_after_date(
        date=date,
        date_range=3,
    )
    available_date_timestamps = [
        available_date.timestamp() * 1000.0
        for available_date in available_dates
    ]
    SOCKET.emit(
        DATE_AVAILABILITY_RESPONSE_CHANNEL,
        {ALL_DATES_KEY: available_date_timestamps},
        room=flask.request.sid,
    )

@SOCKET.on(TIME_AVAILABILITY_REQUEST_CHANNEL)
def on_time_availability_request(data):
    print("Got an event for time input with data:", data)
    date = datetime.datetime.fromtimestamp(data[DATE_KEY] / 1000.0)
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
    date = datetime.datetime.fromtimestamp(data[DATE_KEY] / 1000.0)
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
    )
    end_time = datetime.datetime(
        date.year,
        date.month,
        date.day,
        int(end_time_string.split(":")[0]),
        0,
        0,
    )
    organizer_id = CONNECTED_USERS[flask.request.sid].id
    reservation_success, reservation_code = db_utils.create_reservation(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        organizer_id=organizer_id,
        attendee_ids=attendee_ids,
    )
    print(f"RESERVATION SUCCESS? {reservation_success}")
    print(f"CODE: {reservation_code}")

@APP.route("/")
def index():
    return flask.render_template("index.html")

@APP.route("/overview")
def librarian_overview():
    # TODO: jlh29, ensure that the requesting user has correct permissions
    # i.e. is a librarian
    return flask.render_template("librarian_overview.html")

@SOCKET.on(LIBRARIAN_DATA_REQUEST_CHANNEL)
def on_librarian_data_request(data):
    # TODO: jlh29, ensure that the requesting user has correct permissions
    on_request_appointments(data)
    on_request_rooms(data)
    on_request_users(data)

@SOCKET.on(APPOINTMENTS_REQUEST_CHANNEL)
def on_request_appointments(data):
    # TODO: jlh29, ensure that the requesting user has correct permissions
    # appointments = db_utils.get_all_appointments()
    appointments = []
    SOCKET.emit(
        APPOINTMENTS_RESPONSE_CHANNEL, 
        {APPOINTMENTS_KEY: appointments},
        room=flask.request.sid,
    )

@SOCKET.on(USERS_REQUEST_CHANNEL)
def on_request_users(data):
    # TODO: jlh29, ensure that the requesting user has correct permissions
    # users = db_utils.get_all_users()
    users = []
    SOCKET.emit(
        USERS_RESPONSE_CHANNEL, 
        {USERS_KEY: users},
        room=flask.request.sid,
    )

@SOCKET.on(ROOMS_REQUEST_CHANNEL)
def on_request_rooms(data):
    # TODO: jlh29, ensure that the requesting user has correct permissions
    # rooms = db_utils.get_all_rooms()
    rooms = []
    SOCKET.emit(
        ROOMS_RESPONSE_CHANNEL, 
        {ROOMS_KEY: rooms},
        room=flask.request.sid,
    )

if __name__ == "__main__": 
    db_instance.init_db(APP)
    socket_utils.init_socket(APP)
    SOCKET.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True
    )