"""
    This module manages the active SocketIO instance
"""
import flask_socketio

SOCKET = flask_socketio.SocketIO()


def init_socket(app):
    """
    Initializes the SocketIO instance for a given Flask app
    """
    SOCKET.init_app(app, cors_allowed_origins="*")
