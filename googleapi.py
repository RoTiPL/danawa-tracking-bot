import base64
import pickle
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/spreadsheets'
]

class GoogleAPI:
    def __init__(self):
        """
        Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(DIR_PATH, './token.pickle')):
            with open(os.path.join(DIR_PATH, './token.pickle'), 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(DIR_PATH, './credentials.json'), SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(DIR_PATH, './token.pickle'), 'wb') as token:
                pickle.dump(self.creds, token)


    def get_gmail_service(self):
        service = build('gmail', 'v1', credentials=self.creds)
        return service


    def get_sheet_service(self):
        service = build('sheets', 'v4', credentials=self.creds)
        return service


def create_message(sender, to, subject, message_text):
    """
    Create a message for an email.
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    try:
        return {'raw': base64.urlsafe_b64encode(message.as_string())}
    except:
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8')}


def send_message(service, user_id, message):
    """
    Send an email message.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)


def spreadsheet_read(service, spread_id, range):
    request = service.spreadsheets().values().get(spreadsheetId=spread_id, range=range)
    response = request.execute()
    return response


def spreadsheet_write(service, spread_id, range, value):
    request_body = {
        'values': [
            value
        ]
    }
    request = service.spreadsheets().values().update(spreadsheetId=spread_id, range=range, valueInputOption="USER_ENTERED", body=request_body)
    response = request.execute()
    return response
