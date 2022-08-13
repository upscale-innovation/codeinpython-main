from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from twilio.rest import Client
import os,sys
try:  
   account_sid = os.getenv('account_sid')
   auth_token =  os.getenv('auth_token')
except KeyError: 
   print("Please set the environment variable of account_sid and auth_token")
   sys.exit(1)

client = Client(account_sid, auth_token)

@shared_task
def sleepy(duration):
    sleep(duration)
    return None
    
@shared_task
def send_email_task(subject,message,from_email,recipient_email,fail_silently):
    sleep(30)
    send_mail(
        subject,message,from_email,recipient_email,fail_silently
    )
    return 'Mail sent success'


@shared_task
def send_mobile_task(body,from_,to):
    sleep(30)
    client.messages.create(body, from_, to)
    return 'Mobile OTP sent success'

