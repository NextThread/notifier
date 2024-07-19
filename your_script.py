# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import datetime
# from datetime import timezone
# import json

# # Embedded details.json content
# service_account_info = {
#     "type": "service_account",
#     "project_id": "inte-428705",
#     "private_key_id": "ca887bb11f59914f94704205e8412e9e62ecee93",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQDjWy+HfUHsrSuX\nfD2rR9FoRYHq+6zSrAKLdi7cntRTLD8rvYExwGK4PBKPeJgCNG2T0Ei635vNTV6b\n6Fb1gZL1REOfDWUDToVTRG9m0gkeUSd+5QHlTaBRb7ET1mABB2XzLUuepRosxGxs\nXggVv7hRNJZYx0CXZy/ztvlyS9S7rk2ihlm4EkhAJopx8Knv9Aah7vqC2slHItCJ\nAl4PzbJp90KsVrv6lKyoY/0fmiGFowGUkOJVgK3GYlqG/UefFYPgxiRk5dwZfgZ+\nkXrsPKWR+OvA3As/kL1FMIuab07pDqU3ztOtAfoTvH8fLEuF7jIOJjJ/g52KW9iK\nGKX32yfDAgMBAAECgf8WfJhVU7ARsoIf8roZMgCRFK2rzGaxwipFYUBcYl1BnmHC\n+TIpcnC9gwV6Ng+uPdEoRV84ArOqn1kqjbB7MNGTGI+PfZu0MprLFrVLdBklky53\nZJzQIL7mjAcF0MlFv9khYt2PtN5vbTbtQqNaqpxhlxeupVvG6EMjxXUo7Hj8xE0k\nCs5xoLngZKZ3ioGUO8CKr58HJ4S6Z/i442T6VuEzkwDutEzE7Rw5C531MP5sXub/\nqjIp2/TQm55gLGwZp8j64CDFwpGNzBKuCx1TYmLr/6pd9iPYoKdrSO5hVkhPN9Vu\niYmCVeZHASJNK9QVebR1XDCYjGX+6oMOEk3PV9UCgYEA+JeQ495i00PfhPfFys7Q\nD7lH4tBKpuAZXEulgxdx8iEQHf0QUDVyUAocN40B3YPXvnvaAxajjzwCPW7w6RHC\neK0j/+ln41IbX9j3PqOppoQQUMDRN/9WnQMV2EFmGPEBO8FWaJGyBme0gwwpwaDX\nDGKsO+vN5uZWxpH6gWCR9YcCgYEA6iGeIO8o232019Df2WUk8w6XRNm3hNE82XcH\noqESN8fiXjszpi/DlWTijAHEwR8/jrHVS5i2aGwd8Zu2103epfwIkDIos/CYvE3R\nRipw8RleNqMYSbvnSYocgkFT0rL8Gm7lD0uRasl9BLlKCCiGR0PJpIhXKkchE8KO\nEC2CyuUCgYBvgt21uc4u4qVjahnJjdf7FavPbIvwK1p08mH+Wgf9CyPFr/0fXbo3\neTGLIa+ShE/E3J3BAOjBmbOPhzJ9+j94DoK1iyfU6sHoztSpvpSdY2RGNRgkvF9H\n81hbN4rq6UEaYvG12pU3FlH87vnUJ6gPoDuObYphZzXJwTXTz1PqBQKBgQCpPYW9\nTsNc7aAkhMLatUchPsHPrgT/R/RRSb5GK2Is2hrifK7YCRy6x8MO61RbOQhLUHba\n/1eTYdu/QwzG024G04kpGmjbsSXmr+V/b7xWOz0kB37OBbqpKOF0sl4yJtkfDlwb\nU0eZRm5NVNaT0R9HMlP2z+saD3J0gyUHwq4RlQKBgAvtI4Lf9kZHYPZioqOr470Q\ntRcxhnaGMGARsEI0dmy+ud2r7dQYGhkr0rhchV6JW/vnWrowXCaS86tyvFm7ZU6Z\n8xOQH9Y17ctD9ZKpE6hAm9h7XYAg9kvvrpS/jSin6IPQha2t3DTGHiD0UyQtMUUs\nZUxC3gasqLfUlsNRQ71+\n-----END PRIVATE KEY-----\n",
#     "client_email": "ho-31-423@inte-428705.iam.gserviceaccount.com",
#     "client_id": "106309277416314361208",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ho-31-423%40inte-428705.iam.gserviceaccount.com",
#     "universe_domain": "googleapis.com"
# }

# def check_calendar_and_notify():
#     SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#     creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

#     service = build('calendar', 'v3', credentials=creds)

#     now = datetime.datetime.now(timezone.utc).isoformat()

#     try:
#         events_result = service.events().list(calendarId='primary', timeMin=now,
#                                               maxResults=10, singleEvents=True,
#                                               orderBy='startTime').execute()
#         events = events_result.get('items', [])

#         if not events:
#             print('No upcoming events found.')
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             print(start, event['summary'])
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == '__main__':
#     check_calendar_and_notify()

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from datetime import timezone

def check_calendar_and_notify():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

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
