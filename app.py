import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_socketio
import db_utils
from db_utils import DB
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

@SOCKET.on("date availability")
def on_date_availability(data):
    print("Got an event for date input with data:", data)
    date = datetime.datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    day = str(date.date())
    print(date.date())
    
    #mock avaiable dates
    available_list = {"2020-11-13": ["9:00-11:00", "1:00-3:00"]}
    
    if day in available_list:
        print(day, "is available")
        
        for i in range(len(available_list[day])):
            SOCKET.emit(
                "date status",
                {
                 "time available": available_list[day][i],
                })
    else:
        print(day, "is not available")
        SOCKET.emit("date status", {"is_available": False})
        
@SOCKET.on("time availability")
def on_time_availability(data):
    print("Got an event for time input with data:", data)
    time = data["time"]
    
    print(time)

@APP.route("/")
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    db_utils.init_db(APP)
    socket_utils.init_socket(APP)
    SOCKET.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True
    )