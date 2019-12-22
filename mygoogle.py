import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
calendar_id = '3goiblvs1uhkoghhbmt9t8miug@group.calendar.google.com'

def build_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('googletoken.pickle'):
        with open('googletoken.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('googletoken.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_event_list(service):
    events_result = service.events().list(calendarId=calendar_id, singleEvents=True, orderBy='startTime').execute()
    if events_result:
        print('got event list')
    else:
        print('failed to get event list')
    return events_result.get('items', [])

def insert_event(service, event_body):
    res = service.events().insert(calendarId=calendar_id, body=event_body).execute()
    return res

def update_event(service, event_id, event_body):
    res = service.events().update(calendarId=calendar_id, eventId=event_id, body=event_body).execute()
    return res

def make_event_body(summary, date, description):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'date': date,
        },
        'end': {
            'date': date,
        },
        'reminder': {
            'useDefault': True,
        },
        'transparency': 'transparent',
    }

    return event
