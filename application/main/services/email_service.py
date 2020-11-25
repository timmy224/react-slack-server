from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ...constants.email import email_settings
import smtplib, ssl

def create_email(sender, receiver_email, text, html, subject):
    email = MIMEMultipart("alternative")
    email["subject"] = subject
    email["From"] = email_settings.SENDER_EMAIL
    email["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    email.attach(part1)
    email.attach(part2)

    return email

def send_email(receiver_email, email):
    context = ssl.create_default_context()

    with smtplib.SMTP(email_settings.SMPT_SERVER, email_settings.PORT) as server:
        server.starttls(context=context)
        server.login(email_settings.SENDER_EMAIL, email_settings.PASSWORD)
        server.sendmail(email_settings.SENDER_EMAIL,
                        receiver_email, email.as_string())
