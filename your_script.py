import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from datetime import timezone

def check_calendar_and_notify():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    credentials_path = os.path.expanduser('~/details.json')  # Hardcoded path for testing

    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now(timezone.utc).isoformat()

    try:
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    check_calendar_and_notify()
