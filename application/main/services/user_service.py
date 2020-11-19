from ... import db
from ...models.User import User
from sqlalchemy.orm.exc import NoResultFound

def get_user(username):
    user = User.query.filter_by(username=username).one()
    return user

def get_user_by_email(email):
    try:
        user = User.query.filter_by(username=email).one()
        return user
    except NoResultFound:
        #TODO handle new users
        return 
