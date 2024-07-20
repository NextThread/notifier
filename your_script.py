from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

def check_calendar_and_notify():
    # Define the scopes and service account file
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = '/tmp/service_account.json'
    
    # Authenticate and construct the service
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'  # Query events for the next 7 days
    
    print(f'Getting the upcoming 10 events from {now} to {end_time}')
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=end_time, maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    # Debug: Print the raw events response
    print(f'Raw events response: {events_result}')
    
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

# Run the function
check_calendar_and_notify()
