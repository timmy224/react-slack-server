from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound
import smtplib, ssl
from ...constants.email import email_settings
from . import email_service

def get_user(username):
    return User.query.filter_by(username=username).one()

def get_user_by_email_address(email_address):
    try:
        user = User.query.filter_by(username=email_address).one()
        return user
    except NoResultFound:
        return

def send_new_user_email(inviter, org_name, receiver_email):
    text = email_service.create_text_email(inviter, org_name)
    html = email_service.create_html_email(inviter, org_name)
    message = email_service.create_email_body(inviter, receiver_email, text, html)

    context = ssl.create_default_context()

    with smtplib.SMTP(email_settings.SMPT_SERVER, email_settings.PORT) as server:
        server.starttls(context=context)
        server.login(email_settings.SENDER_EMAIL, email_settings.PASSWORD)
        server.sendmail(email_settings.SENDER_EMAIL, receiver_email, message.as_string())
