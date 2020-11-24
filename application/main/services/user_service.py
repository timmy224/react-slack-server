from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound
import smtplib, ssl
from ...constants.email import email_settings

def get_user(username):
    return User.query.filter_by(username=username).one()

def get_user_by_email(email):
    try:
        user = User.query.filter_by(username=email).one()
        return user
    except NoResultFound:
        #TODO handle new users
        return

def send_email_invite(email):
    receiver_email = email
    message = """\
        Subject: Hi there

        This message is sent from Python.
        """
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(email_settings.SMPT_SERVER, email_settings.PORT, context=context) as server:
        server.login(email_settings.SENDER_EMAIL, email_settings.PASSWORD)
        server.sendmail(email_settings.SENDER_EMAIL, receiver_email, message)
    print("EMAIL SENT")
