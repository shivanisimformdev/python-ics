from services.email import SendEmail
from datetime import datetime


class OrganizeEvent:
    """
    This Event class schedule an event
    and send event as an email with ics attatchement.
    """

    def __init__(self) -> None:
        self.subject = "Event ICS Test"
        self.description = "Testing event"
        self.start_time = datetime(2023,10,12,4,30)
        self.end_time = datetime(2023,10,12,6,30)
        self.attendee_emails = [
            "testing.a@mailinator.com",
            "testing.b@mailinator.com"
        ]
        self.send_reminder_before = 15  # in minutes

    def event_getter(self):
        return {
            "subject": self.subject,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "attendee_emails": self.attendee_emails,
            "send_reminder_before": self.send_reminder_before
        }


if __name__ == "__main__":
    event_organizer = OrganizeEvent()
    data = event_organizer.event_getter()
    email_sender = SendEmail(**data)
    email_sender.send_email()
