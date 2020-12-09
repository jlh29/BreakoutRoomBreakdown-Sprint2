"""
    This module handles sending text message confirmations through Twilio.
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client


class Twilio:
    """
    Send a text to user when reserving an appointment
    """
    dotenv_path = join(dirname(__file__), "twilio.env")
    load_dotenv(dotenv_path)

    TWILIO_ACCOUNT = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH = os.environ["TWILIO_AUTH_TOKEN"]

    twilio_phone = os.environ["TWILIO_PHONE"]
    my_phone = os.environ["MY_PHONE"]

    def __init__(self, number):
        self.to_number = number

    def send_text(self, date, time, attendees, confirmation):
        """
        Sends a text to the organizer's phone containing the details of the
        reservation.
        """
        client = Client(self.TWILIO_ACCOUNT, self.TWILIO_AUTH)

        message = client.messages.create(
            body=(f"Good day! You made a reservation at NJIT Library "
                  f"on {date} at {time} with {', '.join(attendees)}. "
                  f"Your confirmation number is {confirmation}"),
            from_=self.twilio_phone,
            to=self.to_number,
        )
