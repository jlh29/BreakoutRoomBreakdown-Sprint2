import os
from os.path import join, dirname
from dotenv import load_dotenv
from twilio.rest import Client

class Twilio:
    dotenv_path = join(dirname(__file__), "twilio.env")
    load_dotenv(dotenv_path)
    
    twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
    
    twilio_phone = os.environ['TWILIO_PHONE']
    my_phone = os.environ['MY_PHONE']
    
    client = Client(twilio_account_sid, twilio_auth_token)
    
    message = client.messages \
                    .create(
                         body="Hello World from Twilio!",
                         from_=twilio_phone, #twilio phone number
                         to=my_phone  #my real phone number
                     )
   