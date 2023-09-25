import smtplib

import smtplib
from email.mime.multipart import MIMEMultipart
from .ics import ICSGenerator
from decouple import config


class SendEmail:

    def __init__(self, **email_params) -> None:
        self.email_msg = MIMEMultipart()
        self.email_params = email_params

    def set_content(self):
        ics_generator = ICSGenerator(**self.email_params)
        ics_attachment = ics_generator.get_ics_content()
        self.email_msg["Subject"] = self.email_params.get("subject")
        self.email_msg.attach(ics_attachment)

    def send_email(self):
        self.set_content()
        session = smtplib.SMTP(config("SMTP_HOST"), config("SMTP_PORT"))
        session.starttls()
        session.login(config("SENDER_EMAIL"), config("SENDER_PASSWORD"))
        session.sendmail(config("SENDER_EMAIL"), self.email_params.get("attendee"), self.email_msg.as_string())
        session.quit()
