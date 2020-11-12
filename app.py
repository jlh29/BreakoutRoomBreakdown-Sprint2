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

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

dotenv_path = join(dirname(__file__), 'cronofy.env')
load_dotenv(dotenv_path)

cronofy_access_token = os.environ['ACCESS_TOKEN']
calendar_id = os.environ['CALENDAR_ID']

database_uri = os.environ['DATABASE_URL']

APP = flask.Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = database_uri

USERS_UPDATED_CHANNEL = 'users updated'

#Cronofy setup
cronofy = pycronofy.Client(access_token=cronofy_access_token)
events = cronofy.read_events(
    from_date='2020-11-09',
    to_date='2020-11-10',
    tzid='Etc/UTC')
events_result = events.json()
# print(json.dumps(events_result, indent = 2)) 

# display all the evenets in calendar
calendars = cronofy.list_calendars()
# print(json.dumps(calendars, indent = 2)) 

#Create events
event = {
    'event_id': "ABC123",
    'summary': "CS490 Project3 Individual deadline",
    'description': "Finish the individual tasks assigned for MVP",
    'start': "2020-11-11T15:30:00Z",
    'end': "2020-11-11T17:00:00Z",
    'location': {
        'description': "Slack account"
    }
}
cronofy.upsert_event(calendar_id=calendar_id, event=event)


#use endpoints for calendar
endpoint = "https://api.cronofy.com/v1/events?from=2020-11-09&to=2020-11-11&tzid=Etc/UTC"
data = {}
headers = {
    "Authorization": "Bearer {}".format(cronofy_access_token),
    "host": "api.cronofy.com",
}
response = requests.get(endpoint, data=data, headers=headers).json()
# print(json.dumps(response, indent = 2))

# create available periods
endpoint = "https://api.cronofy.com/v1/available_periods"
headers = {
    "Host": "api.cronofy.com",
    "Authorization": "Bearer {}".format(cronofy_access_token),
    "Content-Type": "application/json",
    # "Content-Type": "charset=utf-8",
}
data = {
    "available_period_id": "ROOM1",
    "start": "2020-11-12T9:00:00Z",
    "end": "2020-11-12T11:00:00Z",
}
response2 = requests.post(endpoint, params=data, headers=headers)

# read available periods
endpoint = "https://api.cronofy.com/v1/available_periods?from=2020-11-09&to=2020-11-13&tzid=Etc/UTC"
headers = {"Authorization": "Bearer {}".format(cronofy_access_token)}
data = {
    "host": "api.cronofy.com",
}
response3 = requests.get(endpoint, data=data, headers=headers).json()
print(json.dumps(response3, indent = 2))
    

@SOCKET.on('connect')
def on_connect():
    print('Someone connected!')
    
@SOCKET.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    
@SOCKET.on('new username')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    name=data['name']
    SOCKET.emit('username', {
        'names': name
    })


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