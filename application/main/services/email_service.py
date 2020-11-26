from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

from ...config import config
email_config = config.Config.email

def create_email(receiver_email, text, html, subject):
    email = MIMEMultipart("alternative")
    email["subject"] = subject
    email["From"] = email_config.SENDER_EMAIL
    email["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    email.attach(part1)
    email.attach(part2)

    return email

def send_email(receiver_email, email):
    context = ssl.create_default_context()

    with smtplib.SMTP(email_config.SMPT_SERVER, email_config.PORT) as server:
        server.starttls(context=context)
        server.login(email_config.SENDER_EMAIL, email_config.PASSWORD)
        server.sendmail(email_config.SENDER_EMAIL,
                        receiver_email, email.as_string())
