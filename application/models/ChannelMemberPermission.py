from .. import db, ma
from sqlalchemy import select
from sqlalchemy.orm import column_property
from .ChannelMembers import channel_members
from .User import User
from .OrgChannels import org_channels
from .RolePermissions import role_permissions
from .Permissions import permissions
from .Org import Org
from .Resource import Resource
from .Action import Action
from .Channel import Channel

org_channels_alias = select([
    org_channels.c.org_id.label("org_id_a"),
    org_channels.c.channel_id.label("channel_id_a")
]).alias()

role_permissions_alias = select([
    role_permissions.c.role_id.label("role_id_a"),
    role_permissions.c.permission_id
]).alias()

UserAlias = select([
    User.user_id.label("user_id_a"),
    User.username,
    User.password_hash
]).alias()

permissions_alias = select([
    permissions.c.permission_id.label("permission_id_a"),
    permissions.c.resource_id,
    permissions.c.action_id
]).alias()

ResourceAlias = select([
    Resource.resource_id.label("resource_id_a"),
    Resource.name.label("name_a_resource")
]).alias()

ActionAlias = select([
    Action.action_id.label("action_id_a"),
    Action.name.label("name_a_action")
]).alias()

ChannelAlias = select([
    Channel.channel_id.label("channel_id_a_channel"),
    Channel.name.label("name_a_channel"),
    Channel.is_private,
    Channel.admin_username,
]).alias()

channel_member_permission_join = db.join(channel_members, role_permissions_alias, channel_members.c.role_id == role_permissions_alias.c.role_id_a)\
    .join(UserAlias, channel_members.c.user_id == UserAlias.c.user_id_a)\
    .join(org_channels_alias, channel_members.c.channel_id == org_channels_alias.c.channel_id_a)\
    .join(Org, org_channels_alias.c.org_id_a == Org.org_id)\
    .join(permissions_alias, role_permissions_alias.c.permission_id == permissions_alias.c.permission_id_a)\
    .join(ResourceAlias, permissions_alias.c.resource_id == ResourceAlias.c.resource_id_a)\
    .join(ActionAlias, permissions_alias.c.action_id == ActionAlias.c.action_id_a)\
    .join(ChannelAlias, channel_members.c.channel_id == ChannelAlias.c.channel_id_a_channel)

class ChannelMemberPermission(db.Model):
    __table__ = channel_member_permission_join
    user_id = channel_members.c.user_id
    username = UserAlias.c.username
    channel_id = channel_members.c.channel_id
    org_id = Org.org_id
    org_name = Org.name
    channel_name = ChannelAlias.c.name_a_channel
    resource = ResourceAlias.c.name_a_resource
    action = ActionAlias.c.name_a_action

class ChannelMemberPermissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelMemberPermission
    user_id = ma.auto_field()
    username = ma.auto_field()
    channel_id = ma.auto_field()
    org_id = ma.auto_field()
    org_name = ma.auto_field()
    channel_name = ma.auto_field()
    resource = ma.auto_field()
    action = ma.auto_field()

channel_member_permission_schema = ChannelMemberPermissionSchema()

