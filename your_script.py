import datetime
import io
import smtplib
import time
import pyaudio
import wave
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.cloud import speech

# Google Cloud and Calendar API setup
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "inte-428705",
    "private_key_id": "d6b9c48b1645fd782291ea2b6b34ada3f14961a5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDFuJQC1ELhN7Pd\n/SJbeMRjk7Trh5WyWZ7YZ5Kg9tDPzkGiwQS6mBBs5GXVRSDa//seqnzvEwlTqhch\nfdz7h7dTRLdD/b4Us4lUnZvSNqEmXjlY7BOIklAwNXHJ0jvmg46E7Lf+z0Fj7Zdo\nKQvBt+COIdfDInDKVswAMVXQRCkHGv3vDOVMe3w0bI16Bu6nHILSPjVUifYmGpin\nn40KHX+v681Rb48uUMd2BDR2ujMz9FnRh3McwRF8ewQPDuslBy/T6KlU1VZQNPHy\n1PFOPekZa9zP6uzknzssByaz8pTyGoJvQz7jGLky8FscLpdQpmS1VqK1E8Qu5lZ1\nOwB1fywZAgMBAAECggEABAvfw5PyfY6RuMgWpgaV6eGQFmpU7vOUlWlqHD1tTwNq\nmDynPOZbHs9hzM2qJeodNTTmczPfwRoFP9T/B1Hi8HiJ4A/I//c8NUKM63yH1jO8\nHkWlrZSeT0cm8qszjmdc122SHC+nNiio85VQy7lYaekggg+4RFEmpaOyKx2/UaXC\npP+c592GYeA4LClWnBrRFgB9182wiQ/qedU6wnCjf+sLyjz7nsn2e3Ae+rX1Av1H\nqVIoEaMJKieqCsTXjRhguB97C44XIJUX56zTesIa8atCkZt0z8klybbzSTdsD0I9\nOQr4BKAftVzJ10sLTE2DNAfTg0vEWr2Cw5KUgo9cjQKBgQDyPHIqv3qCKbpJGbOc\n4effigDft+v2LSR9ytCnJwyKhHRNmX5+Cc7oFDxGr6QbQrbVQmRb0GCdGJGFgigw\n97FbrmFBYHDYb+Pg50bWeV4dvA3ra6iksDsz/lIKARX4+fA9hkrAy0FWwt8MKIEN\nDZbaxRrgw85Av0i0L1x35QUUnwKBgQDQ9J4j56uGgn2etnAZhwGjkkA0tFpoztHt\ne7YT6FA7c88ECy71EIY1+2FfcQQI9WeumwxYbLhQcvBOjyZ1mlYDN5+dU/jAuOQ9\nqxF6qhI4SfcaY/p6JTa0Ee7GsLDOBGic+Y+hGZMS6+lVzsF3+mrj99dngpOlcP+w\nBVpZsIEMRwKBgQDHQr3POE94PwcEFuZPCO2KTqVFYq/xg1TfPTTCKzb/wtFA/CC3\nYS4Ybnze0KC34/suFj0j4Zd34rviDR0umrIEbr+F3eU1xWS4nscAqjmnUAhLPfYt\n8uHgdTXbEOWYN1FN6ugXC5ul2QtNnwv5RtJvB3CCr888J52QytzPq06wlQKBgFha\nRo/KApXykSlN3OJ+WmwOiAWBCQVuBgfTmm6aeWpaEnuUOvu2S/mBXG/duqYLFhcX\nSkYNWnXx07h0AQATDTF5EI2WlwTuaNvGfLKQPPn+FHTdN2j0WUgUmRD8XxYNeSp+\nv4OP68dBZz04Gkgf45iXEEadSM7Yk9SavtRTtI07AoGAVQi/y/bnkYaLrlZ1WNNk\nVlrjlDTYAJtRhcwr0ZvYzoUgdP5bm9m9fci6PSwq/2rBFs+l+a99AD4QaEUaTUQh\nOyP1VOs8jD6cZqO+hw8GMXQam1ImJWfz0zaY/YTwLaq7amfSP39hBGhQ/VIL4CP0\nTDrX9Rn0D1aGGIjG7hg8NK8=\n-----END PRIVATE KEY-----\n",
    "client_email": "notifier@inte-428705.iam.gserviceaccount.com",
    "client_id": "112405157857361091396",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/notifier%40inte-428705.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/speech.recognition', 'https://www.googleapis.com/auth/gmail.send']
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)

calendar_service = build('calendar', 'v3', credentials=credentials)
speech_client = speech.SpeechClient(credentials=credentials)

# Email details
EMAIL_ADDRESS = 'anuragroy.dev@gmail.com'
EMAIL_PASSWORD = 'anuragroy880@'

# Function to send email
def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# Function to record audio
def record_audio(filename, duration):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with open(filename, 'wb') as f:
        f.write(b''.join(frames))

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio(filename):
    with io.open(filename, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    response = speech_client.recognize(config=config, audio=audio)

    transcription = ''
    for result in response.results:
        transcription += result.alternatives[0].transcript + '\n'

    return transcription

# Function to check Google Calendar for events
def check_calendar_and_notify():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = calendar_service.events().list(
        calendarId='primary', timeMin=now, timeMax=end_time,
        maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        if 'notifier@inte-428705.iam.gserviceaccount.com' in [attendee.get('email') for attendee in event.get('attendees', [])]:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Found event: {event['summary']} at {start}")
            return event

    print('No upcoming events found.')
    return None

# Main execution loop
while True:
    event = check_calendar_and_notify()
    if event:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        event_duration = 60  # Adjust as needed
        time_until_event = (datetime.datetime.fromisoformat(event_start[:-1]) - datetime.datetime.utcnow()).total_seconds()

        print(f"Waiting for {time_until_event} seconds until the event starts.")
        time.sleep(time_until_event)

        filename = 'meeting_recording.wav'
        print("Recording meeting...")
        record_audio(filename, event_duration)

        print("Transcribing audio...")
        transcription = transcribe_audio(filename)

        print("Sending transcription via email...")
        send_email('anuragr135@gmail.com', 'Meeting Transcription', transcription)

    time.sleep(60)  # Check every minute
