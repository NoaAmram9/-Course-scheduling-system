import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email'
]

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def model_day_to_python_weekday(model_day):
    mapping = {
        1: 6,  # Sunday
        2: 0,  # Monday
        3: 1,
        4: 2,
        5: 3,
        6: 4,
        7: 5,  # Saturday
    }
    return mapping[model_day]

def get_next_date_for_day(model_day, from_date):
    weekday_from = from_date.weekday()
    target_weekday = model_day_to_python_weekday(model_day)
    days_ahead = (target_weekday - weekday_from + 7) % 7
    return from_date + datetime.timedelta(days=days_ahead)

def get_google_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

def export_timetable_to_google_calendar(slot_map, start_date, end_date, calendar_name='Course Schedule', parent=None):
    creds = get_google_credentials()
    service = build('calendar', 'v3', credentials=creds)

    calendar = {
        'summary': calendar_name,
        'timeZone': 'Asia/Jerusalem'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar['id']

    type_color_map = {
        "Lecture": "6",
        "Exercise": "9",
        "Lab": "2",
        "Reinforcement": "11",
        "DepartmentHour": "4",
        "Training": "1",
    }

    # Count total events
    total_events = 0
    for (day_name, hour), _ in slot_map.items():
        model_day = DAYS.index(day_name) + 1
        event_date = get_next_date_for_day(model_day, start_date)
        while event_date <= end_date:
            total_events += 1
            event_date += datetime.timedelta(weeks=1)

    progress = QProgressDialog("Exporting events...", "Cancel", 0, total_events, parent)
    progress.setWindowModality(Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.setWindowTitle("Exporting to Google Calendar...")

    done = 0
    for (day_name, hour), course in slot_map.items():
        model_day = DAYS.index(day_name) + 1
        event_date = get_next_date_for_day(model_day, start_date)
        while event_date <= end_date:
            start_datetime = datetime.datetime.combine(event_date, datetime.time(hour, 0))
            end_datetime = start_datetime + datetime.timedelta(hours=1)

            event = {
                'summary': f"{course['name']} ({course['type']})",
                'location': course['location'],
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Asia/Jerusalem',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Asia/Jerusalem',
                },
                'colorId': type_color_map.get(course['type'], '1')
            }

            service.events().insert(calendarId=calendar_id, body=event).execute()
            done += 1
            progress.setValue(done)

            if progress.wasCanceled():
                print("Export canceled by user.")
                progress.close()
                return

            event_date += datetime.timedelta(weeks=1)

    progress.close()
    print("Export complete!")


#pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
