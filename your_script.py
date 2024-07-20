import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from datetime import timezone

def check_calendar_and_notify():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    with open('/tmp/service_account.json') as f:
        service_account_info = json.load(f)

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    check_calendar_and_notify()
