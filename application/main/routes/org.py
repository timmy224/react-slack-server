from flask import request, jsonify
import json
from .. import main
from ... import db
from ..services import org_service, user_service
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgInvite import org_invite_schema
from ...client_models.org_invite import OrgInviteClient

@main.route("/org/invite", methods=["GET", "POST"])
def invite_to_org():
    """
    [GET] - retrives all outstanding invitations for a user where user is the receipient of an invite
    Path: /org/invite?username={username}
    DB tables: "org_invites"
    [POST] - stores an org invite in the database 
    Request Body: "orgName", "inviterUsername", "email" 
    DB tables: "org_invites"
    """
    if request.method == "GET":
        response = {}
        username = request.args.get("username")
        if username is None: 
            response["ERROR"] = "Missing username in route"
            return response
        org_invites = org_service.get_active_received_org_invites(username)
        org_invites_client = org_service.populate_org_invites_client(org_invites)
        response["org_invites"] = json.dumps(org_invites_client)
        return response
    elif request.method == "POST":
        response = {}
        data = request.json
        org = org_service.get_org(data["orgName"])
        inviter = user_service.get_user(data["inviterUsername"])
        email = data["email"]
        if org_service.has_active_org_invite(org.org_id, email):
            response["ERROR"] = "User already has an active invite to this org"
            return response
        org_invite = org_service.create_org_invite(inviter, org, email)
        org_service.store_org_invite(org_invite)
        response = {"successful": True}
        return jsonify(response)    

@main.route("/org/invite-response", methods=["POST"])
    data = request.json
    #org_name, #username, accepted
    # query where org_name, username, and responded=False 


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

