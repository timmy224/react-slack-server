from flask import request, jsonify
from flask_login import login_required, current_user
import json
from sqlalchemy import and_
from .. import main
from ... import db
from ...models.OrgMemberPermission import OrgMemberPermission, org_member_permission_schema
from ...models.ChannelMemberPermission import ChannelMemberPermission, channel_member_permission_schema
from ..services import permission_service

@main.route("/permissions", methods=["GET"])
# @login_required
def get_permissions():
    # user_id = current_user.user_id
    user_id = request.args.get("user_id")
    org_member_perms = OrgMemberPermission.query().filter_by(user_id=user_id).all()
    channel_member_perms = ChannelMemberPermission.query().filter_by(user_id=user_id).all()
    response = {}
    response["org_member_perms"] = permission_service.gen_org_member_perms_map(org_member_perms)
    response["channel_member_perms"] = permission_service.gen_channel_member_perms_map(channel_member_perms)
    return jsonify(response)

    # interesting thing to think about: organizing channel permissions by what org they're a part of
    # maybe I should add org_id to ChannelPermission (not a bad idea honestly)

    # j = db.session.query(org_members)\
    #     .join(org_channels, org_members.c.org_id == org_channels.c.org_id)
    #     .join(ChannelMemberPermission, (org_members.c.user_id == ChannelMemberPermission.user_id) & (org_channels.c.channel_id = ChannelMemberPermission.channel_id))\
    
    # j = ChannelMemberPermission\
    #     .join(org_channels, ChannelMemberPermission.channel_id == org_channels.c.channel_id)
    #     .join(org_members, )
   
    # ChannelMemberPermission.query.join(channel_members, (ChannelMemberPermission.user_id == channel_members.c.user_id) & (ChannelMemberPermission.channel_id == channel_members.c.channel_id)).filter_by(user_id=user_id) 


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