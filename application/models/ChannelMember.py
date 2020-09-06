from .. import db, ma
from sqlalchemy.orm import column_property
from .User import User
from .Channel import Channel
from .ChannelMembers import channel_members
from .Role import Role

class ChannelMember(db.Model):
    # Role_alias created because of column "name" conflict (both Role and Channel have a "name" column)
    Role_alias = db.select([
        Role.role_id,
        Role.name.label("role_name")
    ]).alias()
    
    j = db.join(User, channel_members, User.user_id == channel_members.c.user_id).\
        join(Role_alias, channel_members.c.role_id == Role_alias.c.role_id).join(Channel, channel_members.c.channel_id == Channel.channel_id)
    
    __table__ = j

    user_id = column_property(channel_members.c.user_id, User.user_id)
    username = User.username
    channel_id = column_property(channel_members.c.channel_id, Channel.channel_id)
    channel_name = Channel.name
    role_id = column_property(channel_members.c.role_id, Role_alias.c.role_id)
    role_name = Role_alias.c.role_name

class ChannelMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelMember
    user_id = ma.auto_field()
    username = ma.auto_field()
    channel_id = ma.auto_field()
    channel_name = ma.auto_field()
    role_id = ma.auto_field()
    role_name = ma.auto_field()
    

channel_member_schema = ChannelMemberSchema()
