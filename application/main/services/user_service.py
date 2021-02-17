from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound
from . import email_service


def get_user(username):
    print(username)
    user = User.query.filter_by(username=username).one()
    return user


def get_user_by_email_address(email_address):
    try:
        user = User.query.filter_by(username=email_address).one()
        return user
    except NoResultFound:
        return


def send_org_invite_email(sender, org_name, receiver_email):
    text = f"""
            Hello!
            Join {org_name} on React Slack
            {sender} has invited you to join the react_slack workspace {org_name} 
            www.react-slack-client.herokuapp.com
            """
    html = f"""
            <html>
                <head>
                </head>
                <body style="text-align:center; color:#434245;">
                    <p style="font-size:1.5rem;">Hello!</p>
                    <h1 style="font-size:2rem;">Join <strong style="background-color: rgb(133, 245, 123); padding: 0px 5px;">{org_name}</strong> workplace on react_slack</h1>
                    <div style="font-size:1rem;">
                        <strong>{sender}</strong> has invited you to join the react_slack workspace <strong>{org_name}</strong>. 
                        <br>
                        Join now to start collaborating!
                    </div>
                    <br>
                    <button style="background-color:#4a154b; font-size:1.5rem; border: 1px solid black; border-radius: 3px; outline: 0; padding: 7px;">
                        <a href="react-slack-client.herokuapp.com" style="text-decoration: none; color:white;">Join Now</a>
                    </button>
                </body>
            </html>
            """
    header = f"{sender}, has invited you to join a react_slack workspace"

    email = email_service.create_email(receiver_email, text, html, header)
    email_service.send_email(receiver_email, email)
