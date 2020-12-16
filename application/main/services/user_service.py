from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound
from . import email_service
from ...models.User import User

def get_user(username):
    return User.query.filter_by(username=username).one()

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
            {sender} has invited you to join the React Slack workspace {org_name} 
            www.reactslack.com
            """
    html = f"""
            <html>
                <body>
                    <p>Hello!</p>
                    <h1>Join {org_name} on React Slack</h1>
                    <p>{sender} has invited you to join the React Slack workspace {org_name}</p>
                    <a href="http://www.reactslack.com">React Slack</a> 
                </body>
            </html>
            """
    header = f"{sender}, has invited you to join a react_slack workspace"

    email = email_service.create_email(receiver_email, text, html, header)
    email_service.send_email(receiver_email, email)

def add_user_db(username, password=None):
    user = User(username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()  

