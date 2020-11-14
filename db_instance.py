# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
def init_db(app):
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()
