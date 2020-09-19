from flask import request, jsonify
import json
from sqlalchemy import and_
from .. import main
from ... import db
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgMemberPermission import OrgMemberPermission, org_member_permission_schema

# EXAMPLES
@main.route("/org/member/", methods=["GET"])
def get_org_members():
    """
    [GET] - grabs a org's org members from the DB and returns it as a JSON response (note that the OrgMember is a join of multiple tables - see OrgMember schema)
    Path: /org/member/?org_id
    Response Body: "org_members"
    DB tables: "users", "org_members", "roles"
    """
    org_id = request.args.get("org_id")
    response = {}
    if org_id is None:
        response["ERROR"] = "Missing org_id in route"
        return response
    org_members = db.session.query(OrgMember).filter_by(org_id=org_id).all()
    response["org_members"] = org_member_schema.dumps(org_members, many=True)
    return response

@main.route("/org/member/permission/", methods=["GET"])
def get_org_member_permissions():
    """
    [GET] - grabs a org member's permissions from the DB and returns it as a JSON response
    Path: /org/member/permission?user_id={user_id}&channel_id={channel_id}
    Response Body: "org_member_permissions"
    DB tables: "org_members", "role_permissions", "permissions", "resources", "actions"
    """
    user_id, org_id = request.args.get("user_id"), request.args.get("org_id")
    response = {}
    if user_id is None:
        response["ERROR"] = "Missing user_id in route"
        return response
    if org_id is None:
        response["ERROR"] = "Missing org_id in route"
        return response
    org_member_permissions = db.session.query(OrgMemberPermission).filter(
        and_(
            OrgMemberPermission.user_id == user_id,
            OrgMemberPermission.org_id == org_id
        )
    ).all()
    response["org_member_permissions"] = org_member_permission_schema\
        .dumps(org_member_permissions, many=True)
    return response