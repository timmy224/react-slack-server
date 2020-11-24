from flask import request, jsonify
from flask_login import login_required, current_user
import json
from sqlalchemy import and_
from .. import main
from ... import db
from ...models.OrgMemberPermission import OrgMemberPermission, org_member_permission_schema
from ...models.ChannelMemberPermission import ChannelMemberPermission, channel_member_permission_schema
from ..services import permission_service

@main.route("/permission/", methods=["GET"])
# @login_required
def get_permissions():
    """
    [GET] - grabs a user's OrgMemberPermissions and ChannelMemberPermissions from the DB. The returned JSON object contains two maps. org_member_perms organizes OrgMemberPermissions by key org_name (value is a list of OrgMemberPermission for that org). channel_member_perms organizes ChannelMemberPermissions by key org_name (value is another map where key is channel_name and value is a list of ChannelMemberPermission)
    Path: /permission/?username={username}
    Response Body: {org_member_perms, channel_member_perms}
    """
    # username = current_user.username
    username = request.args.get("username")
    org_member_perms = db.session.query(OrgMemberPermission).filter_by(username=username).all()
    channel_member_perms = db.session.query(ChannelMemberPermission).filter_by(username=username).all()
    response = {}
    response["org_member_perms"] = permission_service.gen_org_member_perms_map(org_member_perms)
    response["channel_member_perms"] = permission_service.gen_channel_member_perms_map(channel_member_perms)
    return jsonify(response)

# EXAMPLES
@main.route("/permission/org-member/", methods=["GET"])
def get_org_member_permissions():
    """
    [GET] - grabs a org member's permissions from the DB and returns it as a JSON response
    Path: /permission/org-member/?user_id={user_id}&channel_id={channel_id}
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

@main.route("/permission/channel-member/", methods=["GET"])
def get_channel_member_permission():
    """
    [GET] - grabs a channel member's permissions from the DB and returns it as a JSON response
    Path: /permission/channel-member/]?user_id={user_id}&channel_id={channel_id}
    Response Body: "channel_member_permissions"
    DB tables: "channel_members", "role_permissions", "permissions", "resources", "actions"
    """
    user_id, channel_id = request.args.get("user_id"), request.args.get("channel_id")
    response = {}
    if user_id is None:
        response["ERROR"] = "Missing user_id in route"
        return response
    if channel_id is None:
        response["ERROR"] = "Missing channel_id in route"
        return response
    channel_member_permissions = db.session.query(ChannelMemberPermission).filter(
        and_(
            ChannelMemberPermission.user_id == user_id,
            ChannelMemberPermission.channel_id == channel_id
        )
    ).all()
    response["channel_member_permissions"] = channel_member_permission_schema\
        .dumps(channel_member_permissions, many=True)
    return response