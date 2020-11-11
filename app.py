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
import pycronofy
import requests
import json
from datetime import datetime

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

dotenv_path = join(dirname(__file__), 'cronofy.env')
load_dotenv(dotenv_path)

cronofy_access_token = os.environ['ACCESS_TOKEN']
calendar_id = os.environ['CALENDAR_ID']
cronofy_client_id = os.environ['CLIENT_ID']
cronofy_client_secret = os.environ['CLIENT_SECRET']

database_uri = os.environ['DATABASE_URL']

APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = database_uri

USERS_UPDATED_CHANNEL = 'users updated'

#Cronofy setup
# cronofy = pycronofy.Client(access_token=cronofy_access_token)
# cronofy.is_authorization_expired()

# #display the events in date range
# events = cronofy.read_events(
#     from_date='2020-11-10',
#     to_date='2020-11-12',
#     tzid='Etc/UTC')
# events_result = events.json()
# # print(json.dumps(events_result, indent = 2)) 

# # display synced calendars
# calendars = cronofy.list_calendars()
# # print(json.dumps(calendars, indent = 2)) 

# #Create events
# event = {
#     'event_id': "ABC124",
#     'summary': "CS490 Project3 Individual deadline",
#     'description': "Finish the individual tasks assigned for MVP",
#     'start': "2020-11-11T19:30:00Z",
#     'end': "2020-11-11T21:00:00Z",
#     'location': {
#         'description': "Slack account"
#     }
# }
# cronofy.upsert_event(calendar_id=calendar_id, event=event)

@SOCKET.on('connect')
def on_connect():
    print('Someone connected!')
    
@SOCKET.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@SOCKET.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    # TODO
    
@SOCKET.on('date availability')
def on_date_availability(data):
    print("Got an event for date input with data:", data)
    date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    print(date.date())
    
    available_list = ["2020-11-18","2020-11-19","2020-11-20"]
    
    if date in available_list:
        SOCKET.emit("date status", {"is_available": True})
    else:
        SOCKET.emit("date status", {"is_available": False})

@APP.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__': 
    db_utils.init_db(APP)
    socket_utils.init_socket(APP)
    SOCKET.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', '8080')),
        debug=True
    )
