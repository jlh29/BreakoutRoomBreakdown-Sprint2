import flask_socketio

SOCKET = flask_socketio.SocketIO()

def init_socket(app):
    SOCKET.init_app(app, cors_allowed_origins="*")