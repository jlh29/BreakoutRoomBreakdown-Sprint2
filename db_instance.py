"""
    This module manages the active DB instance
"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


def init_db(app):
    """
    Initializes the SQLAlchemy DB for a given Flask app
    """
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()
