import os
from os.path import join, dirname
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGrid:
    dotenv_path = join(dirname(__file__), "sendgrid.env")
    load_dotenv(dotenv_path)
    
    SENDGRID_KEY=os.environ['SENDGRID_API_KEY']
    
    def __init__(self, email):
        self.to_email = email
        
    def send_email(self, date, time, attendees, confirmation):
        body="Good day!<br> You made a reservation at NJIT Library \
                on <strong>{}</strong> at <strong>{}</strong> with {}.<br> \
                Your confirmation number is <strong>{}</strong>" \
                .format(date, time, ', '.join(attendees), confirmation)
                
        message = Mail(
            from_email = 'bcs32@njit.edu',
            to_emails = self.to_email,
            subject = 'Breakout Room Appointment Details',
            html_content = body
            )
            
        try:
            sg = SendGridAPIClient(self.SENDGRID_KEY)
            sg.send(message)
            
        except Exception as e:
            print("Email was not sent!", e)