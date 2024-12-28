import json
from datetime import datetime
import os
from config import settings

class ScheduleManager:
    def __init__(self):
        self.calendar_file = settings.CALENDAR_FILE
        self._ensure_calendar_file()

    def _ensure_calendar_file(self):
        os.makedirs(os.path.dirname(self.calendar_file), exist_ok=True)
        if not os.path.exists(self.calendar_file):
            with open(self.calendar_file, 'w') as f:
                json.dump([], f)

    async def add_event(self, event: dict):
        # Validate event data
        required_fields = ['title', 'date', 'time']
        if not all(field in event for field in required_fields):
            raise ValueError("Missing required fields in event data")

        # Format date and time
        try:
            datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid date or time format")

        # Save event
        with open(self.calendar_file, 'r+') as f:
            events = json.load(f)
            event['id'] = len(events) + 1  # Simple ID generation
            events.append(event)
            f.seek(0)
            json.dump(events, f, indent=2)
            f.truncate()

        return {"message": "Event added successfully", "event_id": event['id']}

    async def get_events(self, date: str = None):
        with open(self.calendar_file, 'r') as f:
            events = json.load(f)
            if date:
                events = [e for e in events if e['date'] == date]
            return events
