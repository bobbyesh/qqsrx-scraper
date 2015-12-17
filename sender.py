import base64
import smtplib
import email
import mimetypes
import os

from apiclient import errors

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user.id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)
