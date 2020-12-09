"""
    This module handles sending emails via Sendgrid.
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGrid:
    """
    Send an email to user, if text message was not sent when reserving an appointment
    """

    dotenv_path = join(dirname(__file__), "sendgrid.env")
    load_dotenv(dotenv_path)

    SENDGRID_KEY = os.environ["SENDGRID_API_KEY"]

    def __init__(self, email):
        self.to_email = email

    def send_email(self, date, time, attendees, confirmation):
        """
        Sends a confirmation email to the organizer containing the details of
        the reservation.
        """
        body = (f"Good day!<br> You made a reservation at NJIT Library "
                f"on <strong>{date}</strong> at <strong>{time}</strong> "
                f"with {', '.join(attendees)}.<br> Your confirmation number is "
                f"<strong>{confirmation}</strong>")

        message = Mail(
            from_email="bcs32@njit.edu",
            to_emails=self.to_email,
            subject="Breakout Room Appointment Details",
            html_content=body,
        )

        try:
            sendgrid_client = SendGridAPIClient(self.SENDGRID_KEY)
            sendgrid_client.send(message)

        except Exception as err:
            print("Email was not sent! ", err)
