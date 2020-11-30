import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client

class Twilio:
    dotenv_path = join(dirname(__file__), "twilio.env")
    load_dotenv(dotenv_path)
    
    TWILIO_ACCOUNT = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH = os.environ['TWILIO_AUTH_TOKEN']
    
    twilio_phone = os.environ['TWILIO_PHONE']
    my_phone = os.environ['MY_PHONE']
    
    def __init__(self, number):
        self.to_number = number
    
    # send reservation details: date, time, attendees, confirmation number
    def send_text(self, date, time, attendees, confirmation):
        client = Client(self.TWILIO_ACCOUNT, self.TWILIO_AUTH)
        
        message = client.messages.create(
            body=" \
            Good day! You made a reservation at NJIT Library" \
            "on {} at {} with {}. Your confirmation number is {}" \
            .format(date, time, attendees, confirmation),
            
            from_=self.twilio_phone, #twilio phone number
            to=self.to_number  #receiver's number
            )