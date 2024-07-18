import datetime
import google.auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(subject, body, to):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = to
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def check_calendar_and_notify():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = Credentials.from_service_account_file('details.json', scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_time = datetime.datetime.fromisoformat(start[:-1])
        reminder_time = event_time - datetime.timedelta(minutes=10)

        if reminder_time <= datetime.datetime.utcnow():
            subject = f"Upcoming Meeting: {event['summary']}"
            body = f"Reminder: You have a meeting '{event['summary']}' at {start}"
            send_email(subject, body, 'your_email@gmail.com')

    return 'Notifications sent.'

if __name__ == "__main__":
    check_calendar_and_notify()
