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

CONNECTED_USERS = {}

@SOCKET.on("connect")
def on_connect():
    print("Someone connected!")
    
@SOCKET.on("disconnect")
def on_disconnect():
    print ("Someone disconnected!")
    CONNECTED_USERS.pop(flask.request.sid, None)
    
@SOCKET.on(USER_LOGIN_CHANNEL)
def on_new_user_login(data):
    print(f"Got an event for new user login with data: {data}")
    # TODO: jlh29, update this
    CONNECTED_USERS[flask.request.sid] = "new user"
    SOCKET.emit(
        SUCCESSFUL_LOGIN_CHANNEL,
        {USER_LOGIN_NAME_KEY: data[USER_LOGIN_NAME_KEY]},
        room=flask.request.sid,
    )

@SOCKET.on(DATE_AVAILABILITY_REQUEST_CHANNEL)
def on_date_availability_request(data):
    print("Got an event for date input with data:", data)
    date = datetime.datetime.fromtimestamp(data["date"] / 1000.0)
    available_dates = db_utils.get_available_dates_after_date(
        date=date,
        date_range=3,
    )
    print(available_dates)
    available_date_timestamps = [
        available_date.timestamp() * 1000.0
        for available_date in available_dates
    ]
    SOCKET.emit(
        DATE_AVAILABILITY_RESPONSE_CHANNEL,
        {"dates": available_date_timestamps},
        room=flask.request.sid,
    )

@APP.route("/")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    db_instance.init_db(APP)
    socket_utils.init_socket(APP)
    SOCKET.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True
    )