import email
from email.mime.base import MIMEBase
import uuid

from icalendar import Calendar, Event, Alarm
from decouple import config


class ICSGenerator:
    """
    ICSGenerator class generates an ics file.
    """
    filename = "event_invite.ics"

    def __init__(self, **event_info):
        self.cal = Calendar()
        self.event = Event()
        self.event_info = event_info
        self.send_reminder_before = event_info.get("send_reminder_before", 15)

    @property
    def calendar_dict(self):
        return {"prodid": "ICS Blog Test", "version": "2.0", "method": "REQUEST"}

    @property
    def event_dict(self):
        return {
            "summary": self.event_info.get("subject"),
            "organizer": config("ORGANIZER_EMAIL"),
            "description": self.event_info.get("description"),
            "dtstart": self.event_info.get("start_time"),
            "dtend": self.event_info.get("end_time"),
            "sequence": 1,
            "uid": uuid.uuid4(),
            "status": "confirmed",
            "attendee;ROLE=REQ-PARTICIPANT": self.event_info.get("attendee_emails"),
            "attendee;ROLE=CHAIR": self.event_info.get("mod"),
        }

    def _add(self, component, cal_data: dict):
        """component: event or cal"""
        for key, value in cal_data.items():
            component.add(key, value)

    def set_alarm(self, event):
        """
        Set a Reminder Alarm before the meeting.
        """
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        if self.send_reminder_before in [0, 5, 15, 30]:
            alarm.add("TRIGGER;RELATED=START", "-PT{0}M".format(self.send_reminder_before))
        if self.send_reminder_before == 60:
            alarm.add("TRIGGER;RELATED=START", "-PT1H")
        if self.send_reminder_before == 120:
            alarm.add("TRIGGER;RELATED=START", "-PT2H")
        if self.send_reminder_before == 720:
            alarm.add("TRIGGER;RELATED=START", "-PT12H")
        if self.send_reminder_before == 1440:
            alarm.add("TRIGGER;RELATED=START", "-P1D")
        if self.send_reminder_before == 10080:
            alarm.add("TRIGGER;RELATED=START", "-P1W")
        event.add_component(alarm)

    def set_ics_data(self):
        self._add(self.cal, self.calendar_dict)
        self._add(self.event, self.event_dict)
        self.set_alarm(self.event)
        self.cal.add_component(self.event)

    def get_ics_content(self):
        self.set_ics_data()
        print(self.event)
        part = MIMEBase("text", "calendar", method="REQUEST", name=self.filename)
        part.set_payload(self.cal.to_ical())
        email.encoders.encode_base64(part)
        part.add_header("Content-Description", self.filename)
        part.add_header("Content-class", "urn:content-classes:calendarmessage")
        part.add_header("Filename", self.filename)
        part.add_header("Path", self.filename)
        return part
