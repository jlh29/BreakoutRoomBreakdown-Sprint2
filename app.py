# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 

USERS_UPDATED_CHANNEL = 'users updated'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

def emit_all_oauth_users(channel):
    all_users = [ \
        user.name for user \
        in db.session.query(models.AuthUser).all()]
        
    socketio.emit(channel, {
        'allUsers': all_users
    })

def push_new_user_to_db(name, auth_type):
    # TODO remove this check after the logic works correctly
    if name != "John Doe":
        db.session.add(models.AuthUser(name, auth_type));
        db.session.commit();
        
    emit_all_oauth_users(USERS_UPDATED_CHANNEL)


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    
    emit_all_oauth_users(USERS_UPDATED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new github user')
def on_new_github_user(data):
    print("Got an event for new github user input with data:", data)
    # TODO

@socketio.on('new facebook user')
def on_new_facebook_user(data):
    print("Got an event for new facebook user input with data:", data)
    # TODO

@socketio.on('new instagram user')
def on_new_instagram_user(data):
    print("Got an event for new instagram user input with data:", data)
    # TODO 
    
@socketio.on('new twitter user')
def on_new_twitter_user(data):
    print("Got an event for new twitter user input with data:", data)
    # TODO

@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    # TODO

@socketio.on('new linkedin user')
def on_new_linkedin_user(data):
    print("Got an event for new linkedin user input with data:", data)
    # TODO

@app.route('/')
def index():
    emit_all_oauth_users(USERS_UPDATED_CHANNEL)
    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
