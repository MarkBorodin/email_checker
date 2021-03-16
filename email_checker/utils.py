import base64
import email
import os
import re
import smtplib
import sys
from typing import List

import dns.resolver
from django.core.mail import send_mail
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from validate_email import validate_email

from app.settings import EMAIL_HOST_USER

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_email_valid(email):
    # Simple Regex for syntax checking
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'  # noqa

    # Email address to verify
    address_to_verify = str(email)

    # Syntax check
    if re.search(regex, address_to_verify):
        return True
    else:
        return False

    # third party library
    # check = validate_email(
    #     email_address=email,
    #     check_format=True,
    # )
    # return check


def check_email_accessible(email):
    check = validate_email(
        email_address=email,
        check_format=True,
        check_smtp=True, smtp_timeout=10,
        check_dns=True, dns_timeout=10,
        smtp_from_address=EMAIL_HOST_USER,
    )
    return check

    # try:
    #
    #     from_address = EMAIL_HOST_USER
    #
    #     # Get domain for DNS lookup
    #     domain = email.split('@')[-1]
    #
    #     # experimental part
    #     # we make a deliberately non-existent email with the required domain
    #     # first_part, second_part = email.split('@')
    #     # fake_email = first_part + 'ashdfabebdfjksjakuahfka' + '@' + second_part
    #
    #     # MX record lookup
    #     records = dns.resolver.resolve(domain, 'MX')
    #     mx_record = records[0].exchange
    #     mx_record = str(mx_record)
    #
    #     # SMTP lib setup (use debug level for full output)
    #     server = smtplib.SMTP()
    #     server.set_debuglevel(0)
    #
    #     # SMTP Conversation
    #     server.connect(mx_record)
    #     server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
    #     server.mail(from_address)
    #     code, message = server.rcpt(str(email))
    #     server.quit()
    #
    #     # Assume SMTP response 250 is success
    #     if code == 250:
    #         return True
    #     else:
    #         return False
    #
    # except Exception:
    #     return False


def check_email_catchall(email):

    try:

        from_address = EMAIL_HOST_USER

        # Get domain for DNS lookup
        domain = email.split('@')[-1]

        # experimental part
        # we make a deliberately non-existent email with the required domain
        first_part, second_part = email.split('@')
        fake_email = first_part + 'ashdfabebdfjksjakuahfka' + '@' + second_part

        # MX record lookup
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange
        mx_record = str(mx_record)

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mx_record)
        server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
        server.mail(from_address)
        code, message = server.rcpt(str(fake_email))
        server.quit()

        # Assume SMTP response 250 is success
        if code == 250:
            return True
        else:
            return False

    except Exception:
        return False

#
# def bounceback_check(required_email):
#
#     try:
#
#         # This opens the authentication json file if it has been created before
#         store = file.Storage('storage.json')
#         creds = store.get()
#
#         # If the credits don't work or don't exist, create them, and
#         # store them for future use. SCOPES are the different parameters
#         # we are granting our API object access to The different scopes can
#         # be found here - https://developers.google.com/gmail/api/auth/scopes
#         SCOPES = 'https://mail.google.com/'
#         if not creds or creds.invalid:
#             flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#             creds = tools.run_flow(flow, store)
#
#         # We create the Gmail API object
#         GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
#
#         # The user_id 'me' indicates  that we are looking at OUR inbox
#         user_id = 'me'
#
#         # The label_id's are the same as those on your actual gmail account
#         # Most are pretty self explanatory, but for a full comprehensive
#         # list, check here: https://developers.google.com/gmail/api/guides/labels
#         label_id_one = 'INBOX'
#         label_id_two = 'UNREAD'
#
#         # We request the unread messages, which is returned to us in a
#         # dictionary (JSON) format I don't know much about the differences
#         # between snake_case vs camelCase, but I noted that the Gmail API
#         # accepts a camelCase variable even from its Python wrapper
#         unread_messages = GMAIL.users().messages().list(
#             userId=user_id, labelIds=[
#                 label_id_one,
#                 label_id_two,
#             ]).execute()
#
#         # We get the messages list from the dictionary of content if it exists
#         try:
#             message_list = unread_messages['messages']
#         except Exception:
#             return False
#
#         # all messages
#         # print(f'{message_list} message_list')
#
#         # Instantiate a list where we will store the emails which bounced back
#         final_list: List = []  # Final list of undeliverable messages
#
#         for message in message_list:
#             message_id = message['id']  # This gets the unique message ID given to each email
#
#             # Fetch the unique message using the API object Payload and header are
#             # parts of the dictionary which is returned by the Gmail API. They
#             # contain the actual content behind each individual email.
#             message = GMAIL.users().messages().get(
#                 userId=user_id, id=message_id
#             ).execute()
#             payload = message['payload']
#             header = payload['headers']
#
#             # current message
#             # print(f'{message} message')
#
#             # Really dirty, but I didn't feel like figuring out a better way to do this
#             # This also cleaned up my code a lot. This just lets me know if I should
#             # actually append this particular message to my list of final messages
#             to_append = True
#
#             # The header contains multiple parts which we iterate through
#             # The one which has key ('name'): value ('Subject') is quite obviously
#             # Where we find our subject for each email
#             # We get the actual string value of the subject, and check for the word
#             # 'Failure', as this is present in every single bounceback email in Gmail
#             # Of course, this may fail on emails which have failure in them, but this works
#             for parts_of_header in header:
#                 if parts_of_header['name'] == 'Subject':
#                     msg_subject = parts_of_header['value']
#                     if 'Failure' in msg_subject:
#                         message = GMAIL.users().messages().get(userId=user_id,
#                                                                id=message_id,
#                                                                format='raw').execute()
#                         message_with_bytes = base64.urlsafe_b64decode(
#                             message['raw'].encode('ASCII'))
#                         email_object = email.message_from_bytes(message_with_bytes)
#                         email_object_as_string = email_object.as_string()
#
#                         if required_email in email_object_as_string:
#                             # This will mark the message as read by removing the label id of 'UNREAD'
#                             GMAIL.users().messages().modify(userId=user_id, id=message_id, body={
#                                 'removeLabelIds': ['UNREAD']}).execute()
#                             return False
#                     # else:
#                     #     to_append = False
#
#             # If it had 'Failure' in the subject, continue
#             # if to_append is True:
#                 # This part took me a while to understand, and isn't very well documented
#                 # aywhere for Python 3. We get the message in a raw format from our Gmail
#                 # API object and then need to encode it into ASCII format, and then decode
#                 # that again (this may be wrong, don't trust me :P). At the end, we obtain
#                 # the email_object as a string with the name email_object_as_string
#                 # message = GMAIL.users().messages().get(userId=user_id,
#                 #                                        id=message_id,
#                 #                                        format='raw').execute()
#                 # message_with_bytes = base64.urlsafe_b64decode(
#                 #     message['raw'].encode('ASCII'))
#                 # email_object = email.message_from_bytes(message_with_bytes)
#                 # email_object_as_string = email_object.as_string()
#                 #
#                 # if required_email in email_object_as_string:
#                 #     # This will mark the message as read by removing the label id of 'UNREAD'
#                 #     GMAIL.users().messages().modify(userId=user_id, id=message_id, body={
#                 #         'removeLabelIds': ['UNREAD']}).execute()
#                 #
#                 #     return False
#
#                 # Here, you can do whatever checks you want to the email, and append it to
#                 # the final list of emails which bounced. I personally used it to check
#                 # for a unique application identifier that I was looking for
#
#                 # final_list.append(email_object_as_string)
#
#             # This will mark the message as read by removing the label id of 'UNREAD'
#             # GMAIL.users().messages().modify(userId=user_id, id=message_id, body={
#             #     'removeLabelIds': ['UNREAD']}).execute()
#
#         return True
#
#     except Exception:
#         return False
#
#
# def send_email_for_check(required_email):
#     send_mail(
#         subject="Hello!",
#         message=':)',
#         from_email=EMAIL_HOST_USER,
#         recipient_list=[required_email],
#         fail_silently=False,
#             )
