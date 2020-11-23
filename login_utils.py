"""
    This module contains some methods to authenticate users and add
    them to the database if necessary.
"""
import os
from os.path import dirname, join
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
import db_utils

load_dotenv(join(dirname(__file__), "oauth.env"))

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_NAME_KEY = "name"
GOOGLE_EMAIL_KEY = "email"

NJIT_DOMAIN = "njit.edu"


def get_user_from_google_token(token):
    """
    Determines whether or not the ID token provided by the user
    is valid. If so, also add them to the database.
    """
    if token is None:
        return None
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        print(
            "The token provided by the client is invalid or the client ID is "
            "incorrectly configured"
        )
        return None

    try:
        ucid, domain = id_info[GOOGLE_EMAIL_KEY].split("@")

        if domain.lower().strip() != NJIT_DOMAIN:
            return None

        user_info = db_utils.add_or_get_auth_user(
            ucid=ucid,
            name=id_info[GOOGLE_NAME_KEY],
        )
        return user_info
    except ValueError:
        print("The email returned by Google (or the obtained user) is invalid")
        return None
