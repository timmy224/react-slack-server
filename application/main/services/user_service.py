from ... import db
from ...models.User import User

def get_user(username):
    return User.query.filter_by(username=username).one()