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
    start_of_day = now.replace(hour=0, minute=0, second=0)
    end_of_day = now.replace(hour=23, minute=59, second=59)

    time_min = start_of_day.isoformat() + 'Z'
    time_max = end_of_day.isoformat() + 'Z'

    print(f"📆 抓取區間：{time_min} ~ {time_max}")

    events_result = service.events().list(
        calendarId='k4ai6134679@gmail.com',  # 使用者的 Gmail 作為 calendarId
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    data = {
        "date": start_of_day.strftime("%Y-%m-%d"),
        "events": []
    }

    for event in events:
        summary = event.get("summary", "(無標題)")
        start_time = event.get("start", {}).get("dateTime", "")
        location = event.get("location", "")
        data["events"].append({
            "summary": summary,
            "start_time": start_time,
            "location": location
        })
        print(f"📝 {summary} @ {start_time} {location}")

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    get_today_events()
