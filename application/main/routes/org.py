from flask import request, jsonify
import json
from flask_login import login_required, current_user
from .. import main
from ... import db
from ..services import org_service, user_service, client_service, role_service, socket_service, permission_service
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgInvite import org_invite_schema
from ...client_models.org_invite import OrgInviteClient
from ...constants.roles import org_roles, channel_roles

@main.route("/org/invite", methods=["POST"])
@login_required
def invite_to_org():
    """    
    [action: GET] - retrives all outstanding invitations for a user where user is the receipient of an invite
    Request Body: "action"
    DB tables: "org_invites"
    [action: STORE] - stores an org invite in the database if user does not already have an active invite to this org
    Request Body: "action", "orgName", "email" 
    DB tables: "org_invites"
    """
    response = {}
    data = request.json
    action = data["action"]
    if action == "GET":
        user = current_user
        org_invites = org_service.get_active_received_org_invites(user.username)
        org_invites_client = org_service.populate_org_invites_client(org_invites)
        response["org_invites"] = json.dumps(org_invites_client)
        return response
    elif action == "STORE":
        response = {}
        org_name = data["orgName"]
        org = org_service.get_org(org_name)
        inviter = current_user
        email = data["email"]
        if org_service.has_active_org_invite(org.org_id, email):
            response["ERROR"] = "User already has an active invite to this org"
            return response
        org_invite = org_service.create_org_invite(inviter, org, email)
        org_service.store_org_invite(org_invite)
        # inform connected client that they've received an org invite
        client = client_service.get_client(email)
        socket_service.send(client, "invited-to-org", org_name)
        response["successful"] = True
        return response

@main.route("/org/invite-response", methods=["POST"])
@login_required
def org_invite_response():
    """
    [POST] - marks an org_invite as responded in the database. If isAccepted is True, adds the user to the org and adds them to all public channels in the org
    Request Body: "orgName", "isAccepted"
    DB tables: "org_invites", "org_members", "channel_members"
    """
    data = request.json
    org = org_service.get_org(data["orgName"])
    user = current_user
    is_accepted = data["isAccepted"]
    org_invite = org_service.get_active_org_invite(org.org_id, user.username)
    org_service.mark_org_invite_responded(org_invite)
    if is_accepted:
        org.members.append(user)
        public_channels = list(filter(lambda c: not c.is_private, org.channels))
        for channel in public_channels:
            channel.members.append(user)
        db.session.commit()
        # get roles
        default_org_role, default_channel_role = role_service.get_role(org_roles.TADPOLE), role_service.get_role(channel_roles.TADPOLE)
        # org members role update        
        statement = role_service.gen_org_members_role_update(org.org_id, user.user_id, default_org_role.role_id)
        db.session.execute(statement)
        # channel members role update
        channel_ids = map(lambda channel: channel.channel_id, public_channels)
        statement = role_service.gen_channel_members_role_update_by_channel_ids(channel_ids, user.user_id, default_channel_role.role_id)
        db.session.execute(statement)
        db.session.commit()
        # inform connected client that they've been added to a new org
        client = client_service.get_client(user.username)
        socket_service.send(client, "added-to-org", org.name)
        permission_service.notify_permissions_updated(user.username)
    else:
        db.session.commit()
    response = {"successful": True}
    return response

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

