from ...models.Role import Role
from ... import db

def get_role(name):
    role = Role.query.filter_by(name=name).one()
    return role
