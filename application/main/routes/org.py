from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import org_service, user_service
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgInvite import org_invite_schema
from ...client_models.org_invite import OrgInviteClient

@main.route("/org/invite", methods=["POST"])
def invite_to_org():
    """    
    [action: GET] - retrives all outstanding invitations for a user where user is the receipient of an invite
    Request Body: "action", "username"
    Path: /org/invite?username={username}
    DB tables: "org_invites"
    [action: STORE] - stores an org invite in the database if user does not already have an active invite to this org
    Request Body: "action", "orgName", "inviterUsername", "email" 
    DB tables: "org_invites"
    """
    response = {}
    data = request.json
    action = data["action"]
    if action == "GET":
        username = data["username"]
        if username is None: 
            response["ERROR"] = "Missing username in route"
            return response
        org_invites = org_service.get_active_received_org_invites(username)
        org_invites_client = org_service.populate_org_invites_client(org_invites)
        response["org_invites"] = json.dumps(org_invites_client)
        return response
    elif action == "STORE":
        response = {}
        org = org_service.get_org(data["orgName"])
        inviter = user_service.get_user(data["inviterUsername"])
        email = data["email"]
        if org_service.has_active_org_invite(org.org_id, email):
            response["ERROR"] = "User already has an active invite to this org"
            return response
        org_invite = org_service.create_org_invite(inviter, org, email)
        org_service.store_org_invite(org_invite)
        response["successful"] = True
        return response

@main.route("/org/invite-response", methods=["POST"])
def org_invite_response():
    """
    [POST] - marks an org_invite as responded in the database. If isAccepted is True, adds the user to the org and adds them to all public channels in the org
    Request Body: "orgName", "username" "isAccepted"
    DB tables: "org_invites", "org_members", "channel_members"
    """
    data = request.json
    org = org_service.get_org(data["orgName"])
    user = user_service.get_user(data["username"])
    is_accepted = data["isAccepted"]
    org_invite = org_service.get_active_org_invite(org.org_id, user.username)
    org_service.mark_org_invite_responded(org_invite)
    if is_accepted:
        org.members.append(user)
        # add to public channels in org
        for channel in filter(lambda c: not c.is_private, org.channels):
            channel.members.append(user)
        # TODO: any socket events for adding to org / channel. will be addressed in near future after add to channel refactor
        # TODO: assign channel member role and org member role (will come after refactor)
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

