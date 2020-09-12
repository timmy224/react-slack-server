from .. import db, ma
from sqlalchemy import select
from sqlalchemy.orm import column_property
from .OrgMembers import org_members
from .RolePermissions import role_permissions
from .Permissions import permissions
from .Resource import Resource
from .Action import Action

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
    Resource.name.label("name_a")
]).alias()

Action_alias = select([
    Action.action_id.label("action_id_a"),
    Action.name.label("name")
]).alias()

j = db.join(org_members, role_permissions_alias, org_members.c.role_id == role_permissions_alias.c.role_id_a)\
    .join(permissions_alias, role_permissions_alias.c.permission_id == permissions_alias.c.permission_id_a)\
    .join(Resource_alias, permissions_alias.c.resource_id == Resource_alias.c.resource_id_a)\
    .join(Action_alias, permissions_alias.c.action_id == Action_alias.c.action_id_a)

class OrgMemberPermission(db.Model):
    __table__ = j
    user_id = org_members.c.user_id
    org_id = org_members.c.org_id
    resource_name = Resource_alias.c.name_a
    action_name = Action_alias.c.name

class OrgMemberPermissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrgMemberPermission
    user_id = ma.auto_field()
    org_id = ma.auto_field()
    resource_name = ma.auto_field()
    action_name = ma.auto_field()

org_member_permission_schema = OrgMemberPermissionSchema()

