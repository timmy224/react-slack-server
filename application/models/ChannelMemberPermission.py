from .. import db, ma
from sqlalchemy import select
from sqlalchemy.orm import column_property
from .ChannelMembers import channel_members
from .OrgChannels import org_channels
from .RolePermissions import role_permissions
from .Permissions import permissions
from .Org import Org
from .Resource import Resource
from .Action import Action

org_channels_alias = select([
    org_channels.c.org_id.label("org_id_a"),
    org_channels.c.channel_id.label("channel_id_a")
]).alias()

role_permissions_alias = select([
    role_permissions.c.role_id.label("role_id_a"),
    role_permissions.c.permission_id
]).alias()

permissions_alias = select([
    permissions.c.permission_id.label("permission_id_a"),
    permissions.c.resource_id,
    permissions.c.action_id
]).alias()

Resource_alias = select([
    Resource.resource_id.label("resource_id_a"),
    Resource.name.label("name_a_resource")
]).alias()

Action_alias = select([
    Action.action_id.label("action_id_a"),
    Action.name.label("name_a_action")
]).alias()

j = db.join(channel_members, role_permissions_alias, channel_members.c.role_id == role_permissions_alias.c.role_id_a)\
    .join(org_channels_alias, channel_members.c.channel_id == org_channels_alias.c.channel_id_a)\
    .join(Org, org_channels_alias.c.org_id_a == Org.org_id)\
    .join(permissions_alias, role_permissions_alias.c.permission_id == permissions_alias.c.permission_id_a)\
    .join(Resource_alias, permissions_alias.c.resource_id == Resource_alias.c.resource_id_a)\
    .join(Action_alias, permissions_alias.c.action_id == Action_alias.c.action_id_a)

class ChannelMemberPermission(db.Model):
    __table__ = j
    user_id = channel_members.c.user_id
    channel_id = channel_members.c.channel_id
    org_id = Org.org_id
    resource_name = Resource_alias.c.name_a_resource
    action_name = Action_alias.c.name_a_action

class ChannelMemberPermissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChannelMemberPermission
    user_id = ma.auto_field()
    channel_id = ma.auto_field()
    org_id = ma.auto_field()
    resource_name = ma.auto_field()
    action_name = ma.auto_field()

channel_member_permission_schema = ChannelMemberPermissionSchema()

