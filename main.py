import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def get_today_events():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds_info = json.loads(os.getenv("CREDENTIALS_JSON"))
    creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow() + timedelta(hours=8)
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=start_of_day, timeMax=end_of_day,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    data = {
        "date": now.strftime("%Y-%m-%d"),
        "events": []
    }

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        time_str = datetime.fromisoformat(start).strftime('%H:%M')
        summary = event.get('summary', '(無標題)')
        data["events"].append({"time": time_str, "summary": summary})

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_today_events()
