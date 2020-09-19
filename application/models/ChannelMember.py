from .. import db, ma
from sqlalchemy.orm import column_property
from .User import User
from .ChannelMembers import channel_members
from .Role import Role
    
channel_member_join = db.join(User, channel_members, User.user_id == channel_members.c.user_id)\
    .join(Role, channel_members.c.role_id == Role.role_id)

class ChannelMember(db.Model):
    __table__ = channel_member_join
    user_id = column_property(channel_members.c.user_id, User.user_id)
    username = User.username
    channel_id = channel_members.c.channel_id
    role_id = column_property(channel_members.c.role_id, Role.role_id)
    role_name = Role.name

class ChannelMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelMember
    user_id = ma.auto_field()
    username = ma.auto_field()
    channel_id = ma.auto_field()
    role_id = ma.auto_field()
    role_name = ma.auto_field()
    
channel_member_schema = ChannelMemberSchema()
