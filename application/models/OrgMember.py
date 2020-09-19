from .. import db, ma
from sqlalchemy.orm import column_property
from .User import User
from .OrgMembers import org_members
from .Role import Role

org_member_join = db.join(User, org_members, User.user_id == org_members.c.user_id)\
    .join(Role, org_members.c.role_id == Role.role_id)

class OrgMember(db.Model):
    __table__ = org_member_join
    user_id = column_property(org_members.c.user_id, User.user_id)
    username = User.username
    org_id = org_members.c.org_id
    role_id = column_property(org_members.c.role_id, Role.role_id)
    role_name = Role.name

class OrgMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrgMember
    user_id = ma.auto_field()
    username = ma.auto_field()
    org_id = ma.auto_field()
    role_id = ma.auto_field()
    role_name = ma.auto_field()

org_member_schema = OrgMemberSchema()