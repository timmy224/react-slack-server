from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound
import smtplib, ssl
from ...constants.email import email_settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_user(username):
    return User.query.filter_by(username=username).one()

def get_user_by_email(email):
    try:
        user = User.query.filter_by(username=email).one()
        return user
    except NoResultFound:
        return

def send_email_invite(inviter, org_name, receiver_email):
    message = MIMEMultipart("alternative")
    message["subject"] = f"{inviter}, has invited you to join a react_slack workspace"
    message["From"] = email_settings.SENDER_EMAIL
    message["To"] = receiver_email

    text = f"""
            Hello!
            Join {org_name} on React Slack
            {inviter} has invited you to join the React Slack workspace {org_name} 
            www.reactslack.com
            """
    html = f"""
            <html>
                <body>
                    <p>Hello!</p>
                    <br>
                    <h1>Join {org_name} on React Slack</h1>
                    <br>
                    <p>{inviter} has invited you to join the React Slack workspace {org_name}</p>
                    <br>
                    <a href="http://www.reactslack.com">React Slack</a> 
                </body>
            </html>
            """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()

    with smtplib.SMTP(email_settings.SMPT_SERVER, email_settings.PORT) as server:
        try: 
            server.starttls(context=context)
            server.login(email_settings.SENDER_EMAIL, email_settings.PASSWORD)
            server.sendmail(email_settings.SENDER_EMAIL, receiver_email, message.as_string())
        except Exception as e:
            print(e)
    print("EMAIL SENT")
