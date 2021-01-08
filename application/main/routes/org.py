from flask import request, jsonify
import json
from flask_login import login_required, current_user
from .. import main
from ... import db
from ..services import org_service, user_service, client_service, role_service, socket_service, event_service
from ...models.OrgMember import OrgMember, org_member_schema
from ...models.OrgInvite import org_invite_schema
from ...client_models.org_invite import OrgInviteClient
from ...constants.roles import org_roles, channel_roles
from ...models.Org import OrgSchema, Org


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
        org_invites = org_service.get_active_received_org_invites(
            user.username)
        org_invites_client = org_service.populate_org_invites_client(
            org_invites)
        response["org_invites"] = json.dumps(org_invites_client)
        return response
    elif action == "STORE":
        response = {}
        org_name = data["org_name"]
        org = org_service.get_org(org_name)
        invited_email_addresses = data["invited_emails"]
        inviter = current_user
        org_service.store_org_invites(inviter, invited_email_addresses, org)
        # inform connected client that they've received an org invite
        org_service.notify_invitees(
            invited_email_addresses, org_name, inviter.username)
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
    user = current_user
    data = request.json
    org_name, is_accepted = data["org_name"], data["is_accepted"]
    org = org_service.get_org(org_name)    
    org_invite = org_service.get_active_org_invite(org.org_id, user.username)
    org_service.mark_org_invite_responded(org_invite)
    if is_accepted:
        org.members.append(user)
        public_channels = list(
            filter(lambda c: c.is_private == "false", org.channels))
        for channel in public_channels:
            channel.members.append(user)
        db.session.commit()
        # get roles
        default_org_role, default_channel_role = role_service.get_role(
            org_roles.TADPOLE), role_service.get_role(channel_roles.TADPOLE)
        # org members role update
        statement = role_service.gen_org_members_role_update(
            org.org_id, user.user_id, default_org_role.role_id)
        db.session.execute(statement)
        # channel members role update
        channel_ids = map(lambda channel: channel.channel_id, public_channels)
        statement = role_service.gen_channel_members_role_update_by_channel_ids(
            channel_ids, user.user_id, default_channel_role.role_id)
        db.session.execute(statement)
        db.session.commit()
        # inform org that a new member has joined 
        event_service.send_new_org_member(org.name, user.username)
        # inform user that they've been added to a new org and org's channels
        socket_service.send_user(user.username, "added-to-org", org.name)
        for channel in public_channels:
            event_service.send_added_to_channel(user.username, channel)
        # inform user that their permissions have been updated        
        event_service.send_permissions_updated(user.username)
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

@main.route("/org", methods=[ "POST", "DELETE"])
@login_required
def orgs():
    """    
    [action: GET] - retrieves all orgs that a user is subscribed to
    Request Body: "action"
    DB tables: "org_members"

    [action: STORE] - store an org into the database if org name is not taken
    Request Body: "action, orgName, invited_emails"
    Info Needed: "orgName, => provided by user needs to be checked for availability
                invites, => create an invite for every invited_member
                members, => should just be current_user
                channels" => set default channel upon entering
    DB tables: "org_members, org_invites, org_channels, org, channel_members"

    ["DELETE"] - delete an org from the database
    Request Body : "org_id"
    DB tables: "org_members, org_invites, org_channels, org"
    """
    if request.method == "POST":
        response = {}
        data = request.json
        action = data["action"]
        if action == "GET":
            is_single_org_get = data.get("org_name")
            if is_single_org_get:
                org = next(filter(lambda org: org.name == data["org_name"], current_user.orgs))
                org_client = org_service.populate_org_client(org)
                response["org"] = json.dumps(org_client)
                return response
            else:
                org_clients = []
                orgs = current_user.orgs
                for org in orgs:
                    org_client = org_service.populate_org_client(org)
                    org_clients.append(org_client)
                response["orgs"] = json.dumps(org_clients)
                return response

        elif action == "STORE":
            org_name = data["org_name"]
            org_is_available = db.session.query(Org.name).filter_by(name = org_name).scalar() is None
            if not org_is_available:
                response["ERROR"] = "Org name is taken"
                return jsonify(response)
            else:
                members = [current_user]
                org = org_service.create_org(org_name, members) 
                org_id = org_service.store_org(org)
                invited_email_addresses = data["invited_emails"]
                inviter = current_user
                org_service.store_org_invites(inviter, invited_email_addresses, org)
                admin_username = current_user.username
                default_channel = org_service.create_default_org_channel(admin_username, members, org)
                admin_org_role, admin_channel_role = role_service.get_role(
                    org_roles.ADMIN), role_service.get_role(channel_roles.ADMIN)
                statement = role_service.gen_org_members_role_update(
                    org.org_id, current_user.user_id, admin_org_role.role_id)
                db.session.execute(statement)
                statement = role_service.gen_channel_members_role_update_by_member_ids(
                    default_channel.channel_id, [current_user.user_id], admin_channel_role.role_id)
                db.session.execute(statement)
                db.session.commit()
                
                org_service.notify_invitees(invited_email_addresses, org_name, inviter.username)
                event_service.send_permissions_updated(inviter.username)
                event_service.send_added_to_org(inviter.username, org_name)
                event_service.send_added_to_channel(inviter.username, default_channel)
                response["successful"] = True
                return response

        elif action == "GET ORG":
            org_name = data["org_name"]
            org = Org.query.filter_by(name = org_name).one()
            org_client = org_service.populate_org_client(org)
            response["org_info"] = json.dumps(org_client)
            return response

    elif request.method == "DELETE":
        data = request.json
        org_name = data["org_name"]
        org = org_service.get_org(org_name)
        org_members = org.members
        org_service.delete_org(org)
        event_service.send_org_deleted(org_name)
        response = { "successful": True}
        return jsonify(response)

